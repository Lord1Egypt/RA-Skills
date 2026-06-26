# Diagnosing gnome-remote-desktop RDP auth failures (server-side first)

**Hard-won lesson:** RDP client error strings are *misleading* for
gnome-remote-desktop. Different server-side causes all collapse into the same opaque
client message. **Always read the server's journald, not the client error.** A prior
session spent effort misattributing this to a "FreeRDP MIC interop bug (#7722),
client-side" — it was actually a stale server credential. Source-code/error-string
reasoning lied; the server log told the truth in one line.

## The misleading client errors (all can mean the same thing)

| Client | Error shown | What it actually means |
|---|---|---|
| RoyalTS | `FREERDP_ERROR_CONNECT_TRANSPORT_FAILED` | usually NLA auth rejected (NOT transport/TLS) |
| FreeRDP CLI | `ERRCONNECT_AUTHENTICATION_FAILED` / `SPNEGO failed` | NLA rejected |
| FreeRDP CLI | `Message Integrity Check (MIC) verification failed` / `SEC_E_MESSAGE_ALTERED` | (historically blamed on a client bug — verify server-side before believing it) |
| any | connects then immediately drops | server tore down after failed NLA |

RoyalTS in particular labels an NLA rejection as a **transport** failure, which sends you
hunting cert/firewall/port problems that are fine.

## The authoritative diagnostic — watch the server during a connect

```bash
# On the box (or over SSH). Follow the service log, then trigger ONE connection attempt.
ssh USER@HOST 'sudo journalctl -u gnome-remote-desktop.service -n0 -f' &
# ...now connect from the client (RoyalTS / xfreerdp /v:HOST /u:USER /p:PW /cert:ignore +auth-only)...
```

### Server log → root cause map

- `ntlm_fetch_ntlm_v2_hash: Could not find user in SAM database`
  `winpr_AcceptSecurityContext: SEC_E_NO_CREDENTIALS`
  → **Stale/empty daemon credentials.** The daemon never loaded the cred you set.
  Fix: `sudo grdctl --system rdp set-credentials <user>` (password via STDIN) **then
  `sudo systemctl restart gnome-remote-desktop.service`** — the running daemon does NOT
  hot-reload creds into its NTLM SAM. (`grdctl status` reads the file and will show the
  *correct* cred the whole time — do not trust it as proof the live daemon has it.)
- `Couldn't retrieve RDP username` → credentials never set at all.
- `Failed to peek routing token: Cancelled` → a client opened TCP then bailed before
  negotiation (e.g. a bare `nc -z` port probe). Benign.
- `BIO_read retries exceeded` / `ERRCONNECT_CONNECT_TRANSPORT_FAILED` *after* a clean NLA
  exchange → the client hung up (normal for `+auth-only` probes). NOT an auth failure.
- A clean attempt that leaves **none** of the `SAM`/`NO_CREDENTIALS` lines → auth succeeded.

## Fast client-side probe (no GUI needed) — separate transport from auth

`+auth-only` completes the NLA handshake and exits without opening a desktop, so it's a
clean auth check. `/sec:tls` forces the security layer to reveal whether NLA is even
required:

```bash
# Does the server REQUIRE NLA? (expected: yes for grd system mode)
xfreerdp /v:HOST:3389 /u:USER /p:PW /cert:ignore +auth-only /sec:tls
#   -> WARN HYBRID_REQUIRED_BY_SERVER  == server demands NLA (correct, expected)

# Does NLA actually authenticate?
xfreerdp /v:HOST:3389 /u:USER /p:PW /cert:ignore +auth-only
#   exit status 1 after a clean exchange (no AUTH_FAILED / MIC line) == auth OK
#   ERRCONNECT_AUTHENTICATION_FAILED / SPNEGO failed                == auth rejected (check server log)
```

## Quick server-health sanity (rules out the non-auth causes in one shot)

```bash
systemctl is-active gnome-remote-desktop.service          # active
sudo ss -tlnp | grep :3389                                # listener bound
sudo grdctl --system status --show-credentials            # username present (file view)
# cert/key match:
sudo openssl x509 -in /var/lib/gnome-remote-desktop/rdp-tls.crt -noout -modulus | md5sum
sudo openssl rsa  -in /var/lib/gnome-remote-desktop/rdp-tls.key -noout -modulus | md5sum   # == cert
```

If service is active, port is bound, cert matches, and creds show in status — but auth still
fails — it's the **stale-credential / needs-restart** case above 95% of the time. Restart the
service first, re-test, *then* keep digging.

## When the server log stays EMPTY — isolate client vs network with tcpdump

If the server's journald shows **nothing** during a client's connect attempt, the client
never reached the daemon — the fault is the client or the path, not grd. Don't guess; packet-
capture on the box settles it in one shot:

```bash
# On the box: capture the RDP port, then trigger ONE connect from the client.
sudo timeout 60 tcpdump -nn -i any 'tcp port 3389' -c 40
```

Read the flags for the client's source IP:

- **No packets at all** → client isn't even dialing the box (wrong host/port in the client
  profile, a stale connection object, DNS, or a client-side error before the socket opens).
- **`SYN -> SYN-ACK -> ACK` then the client sends `FIN`/`RST` with ZERO `length>0` data
  segments** → the client completes the TCP handshake then **tears down before sending any
  RDP/TLS bytes**. This is a **client-side RDP-engine fault**, NOT the server. Seen with
  **RoyalTS / Royal TSX**: every attempt is `[SEW]`/`[.]`/`[F.]` with `length 0`, retried in a
  loop — RoyalTS surfaces it as `FREERDP_ERROR_CONNECT_TRANSPORT_FAILED` even though grd is
  healthy and a plain FreeRDP CLI from the same machine authenticates fine.
  - Prove the server is fine: run `xfreerdp /v:HOST:3389 /u:USER /p:PW /cert:ignore +auth-only`
    from another box — a clean NLA exchange (grd log showing only benign `BIO_read retries
    exceeded`) means the server accepts connections; the GUI client is the problem.
  - RoyalTS fixes to try, in order: **delete & recreate the connection from scratch** (a
    cloned/imported profile can carry a broken transport setting invisible in the UI); disable
    **UDP transport** if the version exposes it (older builds don't); confirm **no Gateway /
    Secure Gateway / "connect through" proxy** is set (check the parent folder too — settings
    inherit); update Royal TSX (embedded FreeRDP connect-time bugs get fixed in newer builds).
- **`SYN` then immediate `RST` from the server, or client data then server `FIN`** → server
  did engage — go back to the server-log -> cause map above.
- **No packets at all from one specific client machine, yet `nc`/SSH to the same host works from
  it, and OTHER hosts RDP fine from it** → the **local VPN stack on that machine is intermittently
  swallowing the RDP connection** (NordVPN, Tailscale, Cloudflare WARP, Zscaler, Little Snitch,
  etc.). These can drop an app's flow at the socket/tunnel layer while plain `nc`/SSH still works,
  so packets never reach the wire. If MULTIPLE different RDP clients all send zero packets, it's a
  system-level VPN/filter, not the app. Tells on macOS: a pile of `utun` interfaces
  (`ifconfig | grep -c '^utun'`), active VPNs in `scutil --nc list`, running helpers
  (`pgrep -fl 'nord|tailscale|warp|zscaler|vpn'`). **Fix: bounce the VPN helper(s)** — e.g.
  `sudo pkill -f -i nordvpn` (and/or restart Tailscale) — which rebuilds the tunnel/filter
  plumbing; re-test after. ⚠️ It's often **stateful/intermittent** (works with the VPN running
  one moment, not the next), so the reliable recovery is bouncing the helper, not trusting a
  single toggle. This is an extremely common "RDP works from machine A but not machine B" root
  cause — check it before blaming the server.

(SSH "REMOTE HOST IDENTIFICATION HAS CHANGED" is a *separate* SSH-only issue — RDP has no
host-key cache. Fix with `ssh-keygen -R <host>` after verifying the new host key is genuine,
e.g. compare network-presented fingerprint to `/etc/ssh/ssh_host_ed25519_key.pub` over an
already-trusted channel. `known_hosts` is per-machine and never synced, so only the laptop with
the stale entry breaks.)

## Two-stage credential model (why "same user+password" still has two prompts)

grd system/headless mode is two-stage by design (grd issue #249): RDP device credential over
NLA → GDM login screen → real Linux user login. NLA (NTLM) and PAM are incompatible, so they
can't be a single credential. We set the **device cred = the Linux user's password** so both
prompts take the same `USER`/password. If the password rotates, re-set the device cred AND
restart the daemon.
