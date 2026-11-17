---
name: magbox
description: "Local dropbox between you and your agent. Move files through two aesthetically pleasing local directories with browser views. A drag-and-drop folder that goes to your agent and a viewable library of what your agent sends to you."
license: MIT
metadata:
  version: "0.2.0"
  envVars:
    - MAGBOX_BIND
    - MAGBOX_PORT
    - MAGBOX_HOSTS
    - MAGBOX_TO_AGENT
    - MAGBOX_FROM_AGENT
    - MAGBOX_MAX_BYTES
    - MAGBOX_MAX_UPLOADS
    - MAGBOX_UPLOAD_TIMEOUT_MS
---

# MagBox

MagBox is a two-way file bridge with no account or external service. **Drop to
Agent** uploads into the inbox; **Drop from Agent** browses and downloads the
outbox. Each view shows current files, counts, total bytes, and modification
times. It is not a durable handoff record: moving, modifying, or removing a file
changes the view. The inbox tray is shared by all clients, not personal history.

## When to use it

- A human needs a non-sensitive document, image, audio file, or export from the
  agent's machine: write it to the configured outbox and return its download URL.
- A long handoff or code block would be awkward to copy from chat: place a `.txt`
  file in the outbox and return its URL.
- A human needs to send the agent a file: return the `/to` page URL.
- Sensitive content (credentials, private records, or confidential documents):
  keep it outside both served directories. Use an approved private channel.
- A short answer: reply inline. An off-network recipient: use an approved
  alternative; do not promise that a local address will work remotely.

## Operating rules

1. Read [README.md](README.md) for first setup and
   [references/deploy.md](references/deploy.md) for services, limits, and routing.
   Install only when requested. Run the server as the directory owner, not root.
2. Check the configured bind and client-reachable address before returning a URL.
   Start from the displayed URL; encode the filename in `/dl/from/<name>`.
   Hostnames work only if the recipient can resolve them and the server allows
   that name. A localhost link works only on the server machine.
3. Never overwrite a previous file. HTTP uploads sanitize filenames and create
   numbered variants. **Direct agent writes bypass that protection.** Use an
   exclusive-create operation and retry with `-v2`, `-v3` before the extension
   when the destination exists. A directory listing followed by an ordinary
   write does not provide collision protection.
4. The directories are dedicated to handoffs and controlled by their local
   owner. Do not use symlinks, nested inbox/outbox paths, or folders other local
   users can modify. Do not leave sensitive data in either directory.
5. Cleanup is local only. Preview the exact files and confirm with the human
   before removal. There is no browser delete route, automatic expiry, or trash
   managed by MagBox.

## Network boundary

The default listener is `127.0.0.1:9900`. LAN exposure is an explicit setup choice.
**Anyone reaching the port can read served files and upload into the inbox.**
Host and Origin checks reduce browser-driven abuse; they are not authentication.
Do not expose the service on public/shared networks or forward its raw port to
the internet. `0.0.0.0` listens on all IPv4 interfaces, not just a LAN.

For a VPN, bind to the host's VPN interface address with access restricted by VPN
policy, or keep loopback and configure a specific private forwarding arrangement.
Loopback binding by itself does not make the service reachable over a VPN.
MagBox supplies no authentication, TLS, cloud sync, or per-file permissions.
