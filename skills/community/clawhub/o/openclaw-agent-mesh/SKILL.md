---
name: openclaw-agent-mesh
description: Peer discovery and agent-to-agent communication for OpenClaw instances. Use when the user wants nearby OpenClaw nodes to discover each other, request contact, require explicit approval, establish trust, and exchange direct messages. Supports V1 workflows for identity initialization, LAN scanning, contact requests, request approval/rejection, point-to-point messaging, and a lightweight HTTP server for discovery and inbox handling.
---

# OpenClaw Agent Mesh

Provide a minimal but real agent-to-agent communication layer for OpenClaw instances.
Use the bundled scripts to initialize identity, scan a local network range, exchange contact requests, approve peers, and send signed direct messages.
Require explicit acceptance before trusted communication begins.

## V1 scope

Implement only these capabilities:
- local identity generation
- LAN discovery by probing peer endpoints
- contact request creation
- contact approval or rejection
- trusted peer storage
- direct signed message creation and delivery
- inbox verification and acknowledgement
- lightweight HTTP server for discovery, contact-request intake, and message intake

Do not claim NAT traversal, full mesh routing, or multi-party consensus in V1.

## Files and local state

Store mesh state outside the skill folder.
Use this default path unless the user specifies another one:
- `~/.openclaw/agent-mesh/`

Expected files:
- `identity.json` — local agent identity
- `private_key.pem` — local signing key
- `peers/<agent_id>.json` — trusted peers
- `requests/incoming/*.json` — pending inbound contact requests
- `requests/outgoing/*.json` — outbound contact requests
- `messages/incoming/*.json` — verified inbound messages
- `messages/outgoing/*.json` — sent messages
- `groups/` — reserved for future versions

## Workflow

### 1. Initialize local identity

Run `scripts/mesh.py init`.
This creates a signing keypair and an identity card with:
- `agent_id`
- `display_name`
- `public_key`
- `endpoint`
- `created_at`
- `fingerprint`

Set the endpoint to a reachable HTTP URL if the node should receive requests from peers.

### 2. Scan for nearby peers

Run `scripts/mesh.py scan` with a base URL template or a list of candidate URLs.
Scanning in V1 is HTTP discovery, not raw port scanning.
Probe each candidate at:
- `/agent-mesh/discovery`

Treat discovered nodes as untrusted until approved.

### 3. Send a contact request

Run `scripts/mesh.py request-contact`.
Send a signed request to a discovered node’s inbox endpoint.
The receiver stores the request as pending.

### 4. Approve or reject the request

Run `scripts/mesh.py list-requests` then `approve-request` or `reject-request`.
Approval writes the peer into the trust store.
Rejection leaves no trusted relationship.

### 5. Send a direct message

Run `scripts/mesh.py send-message` only after trust exists.
The sender signs the message envelope.
The receiver verifies signature, timestamp, and trust status before accepting.

### 6. Verify delivery

Run `scripts/mesh.py list-messages` or inspect stored message JSON files.
Use acknowledgements to confirm receipt.

## Transport model

V1 uses simple HTTP JSON endpoints:
- `GET /agent-mesh/discovery`
- `POST /agent-mesh/contact-request`
- `POST /agent-mesh/message`

Run `scripts/server.py` to expose these endpoints from a node that should be discoverable or receive peer traffic.
Example:
- `python3 scripts/server.py --host 0.0.0.0 --port 8787 --state-dir ~/.openclaw/agent-mesh`

If the user does not yet have a server to receive HTTP traffic, use the scripts to generate and inspect signed payloads locally first.

## Guardrails

- Require explicit approval before trusting a peer.
- Never auto-accept unknown peers.
- Never send private keys over the network.
- Prefer signed JSON envelopes with timestamps and message IDs.
- Reject stale or malformed messages.
- Keep V1 limited to point-to-point trust and messaging.

## References

- Read `references/protocol.md` for the JSON message model.
- Read `references/verification.md` for trust and signature checks.

## Deliverables

When using this skill, produce one or more of:
- a configured local mesh identity
- a peer discovery result set
- a pending or approved contact request
- a verified direct-message flow
- a troubleshooting checklist for failed trust or message delivery
