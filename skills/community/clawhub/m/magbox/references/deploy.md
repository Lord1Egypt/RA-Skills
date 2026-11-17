# MagBox deployment

## Configuration

| Variable | Default | Meaning |
| --- | --- | --- |
| MAGBOX_BIND | 127.0.0.1 | Listening interface/address; explicit LAN opt-in |
| MAGBOX_PORT | 9900 | 0–65535; 0 selects a temporary port for tests |
| MAGBOX_HOSTS | empty | Extra exact DNS names or addresses, comma-separated, no port or scheme; IPv6 in brackets |
| MAGBOX_TO_AGENT | ~/Inbox | Human uploads; tilde here describes the home default |
| MAGBOX_FROM_AGENT | ~/Outbox | Agent files for download |
| MAGBOX_MAX_BYTES | 16777216 | Entire upload request cap, 1–268435456 bytes |
| MAGBOX_MAX_UPLOADS | 2 | Simultaneous uploads, 1–8 |
| MAGBOX_UPLOAD_TIMEOUT_MS | 30000 | Total body-receive deadline, 50–300000 ms |

Environment directory values use real absolute paths (shell-expanded `$HOME`
works; a literal tilde in a service setting does not). Use separate, non-nested
local directories under the same trusted owner's control. Remote/network
filesystems are outside the supported collision and file-identity guarantees.
Final symlinks and nonregular files are rejected. File descriptors, identity
checks, and canonical-root checks reduce path races; this service is not a
sandbox against a malicious local user who can change its storage directories.

Uploads are buffered only within the byte and concurrency caps, then parsed
before writing. Budget memory for roughly twice the configured bytes per active
upload plus runtime overhead. Raise both caps cautiously. At most eight file
parts and 8 KiB of headers per part are accepted. Filename sanitization keeps
ASCII letters/digits, dot, underscore, and dash; other characters become
underscores. Empty/dot names, the internal `.magbox-` prefix, and sanitized names
longer than 200 bytes are rejected. Collisions after sanitization also version.
HTTP uploads use exclusive creation and retry numbered suffixes. Direct outbox
writes need their own no-overwrite discipline.

A failed multi-file upload rolls back files it created; files still being saved
are withheld from the browser. Disconnects before completion also trigger
cleanup. A process kill/power loss can leave an incomplete file; inspect locally
before restarting after a crash. No automatic cleanup runs on startup.

Specific binds are automatically permitted Host names, along with localhost and
loopback addresses. Wildcard binds (`0.0.0.0` or `::`) also need `MAGBOX_HOSTS`.
Hosts must use the actual listener port. Browser uploads must be same-origin;
non-browser clients can omit Origin. These rules are not authentication. For a
VPN, bind to its interface with peer access controlled by VPN policy, or configure
an explicit private forwarder to loopback. There is no built-in forwarding or TLS.

## Routes

| Method | Path | Result |
| --- | --- | --- |
| GET | / or /from | Dark outbox grid |
| GET | /to | White upload page and collapsed inbox tray |
| GET | /api/from | Outbox `{files, count, totalBytes}` |
| GET | /api/to/list | Inbox `{files, count, totalBytes}` |
| GET/HEAD | /dl/from/NAME | Outbox file; URI-encode NAME |
| GET/HEAD | /dl/to/NAME | Inbox file; URI-encode NAME |
| POST | /api/to | Multipart fields named file; JSON `{saved:[{name,size}]}` |

There is no delete route. Lists describe current files and modification times,
not immutable handoff events. Listing response envelopes and upload JSON differ
from v0.1; update custom clients when replacing that version.

GET supports one closed, open-ended, or suffix byte range. Invalid, multiple,
and unsatisfiable ranges return 416. HEAD reports the complete resource and
ignores Range as specified for methods other than GET. Unknown types, SVG, and
PDF are attachments with a restrictive sandbox policy; raster thumbnails and
common audio/video types can be inline. Every download uses `nosniff`.

## Services

Do not install both services. Run as your ordinary user. Set real absolute paths
and save any intended directory/network overrides in the service environment.

### macOS launchd

Edit the Node path, server path, and both log paths in `templates/magbox.plist`.
Use an owner-controlled log directory, such as your existing `~/Library/Logs`,
expressed as an absolute path in the plist. The default bind is explicit.
For LAN use, replace it with the private interface address; optionally add
`MAGBOX_HOSTS` in the same EnvironmentVariables dictionary.

```sh
mkdir -p "$HOME/Library/LaunchAgents"
cp templates/magbox.plist "$HOME/Library/LaunchAgents/ai.magbox.plist"
plutil -lint "$HOME/Library/LaunchAgents/ai.magbox.plist"
launchctl bootstrap "gui/$(id -u)" "$HOME/Library/LaunchAgents/ai.magbox.plist"
```

Stop: `launchctl bootout "gui/$(id -u)/ai.magbox"`.
Restart a loaded service: `launchctl kickstart -k "gui/$(id -u)/ai.magbox"`.
After changing its plist, boot out and bootstrap again. Logs use the two configured
paths. A user LaunchAgent starts at login; it is not a boot-before-login daemon.

### Linux systemd user service

Edit the Node and server paths in `templates/magbox.service`. The template uses
the logged-in user's account; do not add a system-level root service. Replace
`MAGBOX_BIND` for LAN use and add `MAGBOX_HOSTS` only when needed.

```sh
mkdir -p "$HOME/.config/systemd/user"
cp templates/magbox.service "$HOME/.config/systemd/user/magbox.service"
systemctl --user daemon-reload
systemctl --user enable --now magbox.service
```

Stop: `systemctl --user stop magbox.service`.
Restart: `systemctl --user restart magbox.service`.
Logs: `journalctl --user -u magbox.service -n 50`.
After edits, reload the user manager before restarting. Persistence beyond logout
depends on the host's user-session policy; this package does not change it.

After either install, verify locally with `curl http://127.0.0.1:9900/api/from` for
loopback binding, or substitute the specific configured private address. Verify
both page URLs from a second device only after deliberately enabling LAN access.
