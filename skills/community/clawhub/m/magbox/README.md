# MagBox 0.2.0

Two folders, two browser views, zero added dependencies. The white **Drop to
Agent** page uploads into an inbox and has a collapsed tray of current inbox
files. The dark **Drop from Agent** page shows an outbox with previews and
individual downloads. Both show file counts, total bytes, and modification times.
These are current directory views, not a durable handoff record.

## Start on the host

Use Node.js 22 or later on macOS or Linux. Tested with Node.js **22.23.2** on macOS.
No package installation step is needed. From this package directory:

```sh
node --version
node scripts/magbox-server.mjs
```

Keep the process running. Defaults are `~/Inbox`, `~/Outbox`, and loopback port
9900. The directories are created if absent. New directories are owner-only;
existing directory permissions are unchanged. Keep these folders dedicated to
non-sensitive handoffs and controlled by their local owner. Do not run as root.

On the same machine open:

- Outbox/downloads: <http://127.0.0.1:9900/>
- Inbox/uploads: <http://127.0.0.1:9900/to>

The foreground prints both addresses. Verify with:

```sh
curl http://127.0.0.1:9900/api/from
```

An empty outbox returns `{"files":[],"count":0,"totalBytes":0}`.

## Try both directions

1. Choose a non-sensitive test file on `/to`. The status shows its saved filename;
   open the tray to see it in the inbox. Upload it twice to see `-v2` versioning.
2. Place a different non-sensitive file in `~/Outbox` without replacing an
   existing file. Refresh `/` and select Download. Direct agent/shell writes must
   use their own exclusive-create mechanism; server upload versioning does not
   apply to those writes.

Default uploads allow 16 MiB per HTTP request including multipart overhead and
up to two simultaneous requests. The browser sends selected files sequentially.
Larger downloads stream; media GETs support a single byte range. SVG and unknown
formats download as opaque attachments, not active previews.

## Enable a trusted LAN deliberately

**There is no authentication or TLS. Anyone reaching the port can read served
files and upload into the inbox.** Keep sensitive files outside both directories.
Host/Origin checks are browser defenses, not authentication. Never forward the
raw port to the internet or use it on a public/shared network.

Stop the foreground process with Ctrl-C. Substitute the host's actual private
interface address for the example, then start:

```sh
MAGBOX_BIND=192.168.1.20 node scripts/magbox-server.mjs
```

From the other machine open `http://192.168.1.20:9900/` and
`http://192.168.1.20:9900/to`. If using a resolvable hostname, allow it explicitly:

```sh
MAGBOX_BIND=192.168.1.20 MAGBOX_HOSTS=agent-host.local node scripts/magbox-server.mjs
```

`0.0.0.0` means **all IPv4 interfaces**. If choosing that bind, also set
`MAGBOX_HOSTS` to the actual names/addresses clients will use and restrict the
port using the host firewall. Prefer a specific private address.

For a VPN, bind to the host's VPN interface address and restrict reachable peers
using VPN policy. Alternatively, keep loopback and deliberately configure a
private tunnel/forwarder to `127.0.0.1:9900`; permit its client-facing Host using
`MAGBOX_HOSTS`. Loopback alone is not reachable from another VPN device.

## Keep it running, stop it, inspect logs

The installed server is the single `scripts/magbox-server.mjs` file: keep it at a
stable absolute path. No HTML files or dependencies must accompany it.
[Service instructions](references/deploy.md#services) cover the
[macOS template](templates/magbox.plist) and
[Linux template](templates/magbox.service), including stop/restart and logs.
Foreground logs go to the terminal. Ctrl-C stops the foreground listener.

## Cleanup

No browser deletion, automatic expiry, or server-managed trash is provided.
Counts and bytes help identify growth. Use a local file manager to preview the
exact selected files, confirm the selection with the human, then move them to
the system Trash. For shell cleanup, list and review explicit paths first and
confirm before removal; do not use an unreviewed wildcard. Clearing a directory
removes those entries from the browser immediately on Refresh.

## Troubleshooting

- Connection refused: check the process/service and bind/port settings.
- Works locally only: default loopback cannot accept a second machine; opt into
  the private interface and check the firewall and network isolation settings.
- Hostname does not resolve: use the configured private address or fix local DNS/
  mDNS. A printed hostname is not a guarantee that another device can resolve it.
- HTTP 403 Host: use an allowed address and the actual port; add a client-facing
  name via `MAGBOX_HOSTS`. Forwarders must preserve a permitted Host and the
  matching HTTP Origin. Arbitrary external Origin values are rejected.
- HTTP 413/429/408: see [limits](references/deploy.md#configuration). Reduce file
  size, wait for other uploads, or adjust the receive timeout within its bounds.
- Files absent: subdirectories, symlinks, special files, and pending uploads are
  excluded. On-disk files with invalid names are not served.
- Storage error: inspect directory permissions, available disk space, and the
  local log. A replaced/moved storage root needs configuration review and restart.
- Interrupted transfer: refresh before retrying; a completed upload whose reply
  was lost can already exist. Retrying creates another numbered copy.

Regression tests use only Node built-ins: `node --test tests/magbox.test.mjs`.
Scanner status is recorded separately with the sandbox delivery; no hosted scan
or registry publication is performed by these tests.
