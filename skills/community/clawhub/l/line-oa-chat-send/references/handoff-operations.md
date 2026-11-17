# Handoff operations

Why the session and handoff scripts look the way they do. Everything here is
already enforced in code — this is the reasoning, for when the code needs
changing. Read it before editing `scripts/start_line_oa_chromium.sh`,
`scripts/start_line_oa_vnc_handoff.sh`, or `scripts/lib/*.sh`.

## Shape

```
Browser session (long-lived, loopback only)
  Xvfb ── Chromium ── CDP 127.0.0.1:9222
    └──── x11vnc ──── websockify ──── Caddy (404 until armed)

Login handoff (ephemeral, the only thing that is ever externally reachable)
    Caddy token route ──── cloudflared Quick Tunnel ──── public HTTPS URL
```

The session owns the browser. The handoff attaches. Revoking the handoff removes
the tunnel and the route and leaves everything else running.

## Ports are never assumed free

VNC, websockify, Caddy, and Caddy's admin endpoint all get dynamically selected
loopback ports, chosen in one call that holds each socket until all are chosen —
otherwise the same port can be handed out twice.

Fixed ports silently attach the handoff to something else. A hard-coded `5900`
can bind to another display and produce a black canvas; a hard-coded front-end
port can collide and leave a working tunnel URL serving nothing.

## Caddy's output is not discarded

A bind conflict with output sent to `/dev/null` surfaces as "the URL works but
the page is blank" — expensive to diagnose, trivial to prevent. Output goes to
the run log.

## The site address is host-agnostic

```
:PORT {
  bind 127.0.0.1
  ...
}
```

Not `http://127.0.0.1:PORT`. The tunnel arrives carrying a public Host header,
and a host-specific site address rejects it. `bind 127.0.0.1` keeps the listener
on loopback while leaving the matcher host-agnostic.

Keep `handle` blocks multi-line. Compact inline blocks can fail Caddy parsing.

## x11vnc needs `-noxrecord -noxfixes -noxdamage`

Without them noVNC can stay black even while Chromium has a mapped window on the
display.

The cost is real: `-noxdamage` disables the damage extension, so x11vnc polls
the whole screen instead of being told what changed. That means higher CPU and a
less responsive remote canvas. It is a deliberate trade — a slow picture beats no
picture — and it affects interaction latency, not startup time.

## Verification waits before it probes

The single most counterintuitive part.

A fresh `trycloudflare.com` hostname is **not resolvable when cloudflared prints
it**. A lookup that misses is cached as a negative answer, and re-querying keeps
refreshing that negative entry — so an eager polling loop holds itself in
failure long past actual propagation.

Measured:

| Approach | Outcome |
| --- | --- |
| Probe immediately, poll every 1s | Hostname never resolved within 120s |
| Wait 45s quietly, then query once | Resolved on the first query |

This is not a container artifact. systemd-resolved, dnsmasq, and container
embedded DNS all cache negative answers.

So the handoff waits a quiet grace window (`LINE_OA_SEND_CHAT_HANDOFF_VERIFY_GRACE`,
default 5s) before its first lookup, then backs off progressively, and records
DNS resolution as a phase separate from HTTP reachability — they are different
waits with different causes.

### There is no propagation floor to clear

The obvious model — propagation takes about N seconds, so wait N — does not
survive measurement. Target host, three runs at each value plus three baseline
runs at the 20s default:

| grace | first-lookup hits | `url_verified` when it hit |
| --- | --- | --- |
| 5s | 3/3 | ~10.7s |
| 8s | 3/3 | ~13.3s |
| 12s | 3/3 | ~16.7s |
| 16s | 2/3 | ~20.5s |
| 20s | 3/3 sweep, 2/3 baseline | ~25.4s |

Two misses in 18 runs, ~11%, and both were large outliers: the lookup took
40–60s longer than the grace, not slightly longer.

So propagation completed inside 5s for at least nine consecutive tunnels, and
the 20s run that missed waited 60s — four times the grace would not have saved
it. Waiting longer costs ~15s on every fast arm and does not buy protection on
the slow ones.

Do not read the misses landing on the two longest values as evidence that longer
is *worse*. With three runs each that is well within chance. The defensible
reading is that misses look independent of the grace window.

Hence: a short grace, and a backoff that recovers when an outlier appears. It
does recover — the 16s miss verified at 61s rather than failing.

Typical successful arm at the 5s default:

```
route_armed     0.03s
tunnel_url      4.60s   URL printed here, and not yet usable
dns_resolved    9.60s   resolved on the first query after the grace window
url_verified   10.70s   HTTP succeeded on the first attempt
```

## A local request is not verification

`curl http://127.0.0.1:<caddy-port>/...` proves the local chain works. It says
nothing about whether the tunnel carries traffic. The script fetches the **public
URL** and requires HTTP 200 with noVNC content before printing anything.

Nothing is printed on failure. The script revokes what it started and exits
non-zero naming the phase.

## Phase timing

Every run of the session and handoff scripts writes a phase log to
`$RUNTIME_DIR/timing/`, mode 600, with phase names and durations only — never a
URL, route token, or credential. There is no debug flag, because the slow runs
are the ones nobody thought to instrument.

## Chromium's SingletonLock

Chromium writes a `SingletonLock` symlink into the profile recording
`<hostname>-<pid>`. A hard-killed Chromium leaves it behind.

- Same hostname, dead PID → stale; the session start clears it and says so.
- Different hostname → **not** cleared. Another Chromium may genuinely hold the
  profile, and clearing it could corrupt a live session. Reported distinctly so
  the cause is obvious rather than surfacing as a generic launch failure.

This bites in containers especially, where a random per-container hostname makes
every rerun look like "in use on another computer".

## Chromium in a container

Two concessions apply to the test environment only, never to a real host:
`--security-opt seccomp=unconfined` (Docker's default filter blocks the
namespace creation the zygote needs) and `--shm-size` (Chromium exhausts the
64MB default). See `containers/README.md`. Neither is a reason to teach the
scripts a container-only flag.

## Running as root

Chromium refuses to start as root with its sandbox enabled
(`Running as root without --no-sandbox is not supported`).

The fix is to run unprivileged, under a service identity that owns the profile
directory. That is how the browser is meant to run anyway.

```bash
useradd --create-home --uid 1000 lineoa
chown -R lineoa:lineoa /opt/data/chromium
su - lineoa -c 'cd <repo> && bash scripts/start_line_oa_chromium.sh'
```

For deployments that genuinely cannot drop privileges — a pod fixed to root, for
instance — there is an explicit opt-in:

```bash
LINE_OA_SEND_CHAT_ALLOW_NO_SANDBOX=1 bash scripts/start_line_oa_chromium.sh
```

It is opt-in and it warns on every start, because the cost is not theoretical.
Ordinarily this browser only visits `chat.line.biz`, so a disabled renderer
sandbox has little to contain. **A login handoff changes that**: it grants
interactive control, so whoever holds the URL can navigate the browser anywhere,
and an unsandboxed renderer contains far less of whatever they reach. The same
browser holds the authenticated LINE session.

If you must run this way, keep handoffs short and treat the URL with more care,
not less.
