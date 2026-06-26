---
name: myr
version: 1.3.0
description: Capture, search, verify, export, import, and synthesize Methodological Yield Reports (MYRs) for OODA-based intelligence compounding. Use when: (1) installing MYR on a node, (2) storing yield from OODA cycles, (3) searching prior yield before new work, (4) operator-reviewing MYR quality, (5) exporting/importing signed MYRs between nodes, (6) running the HTTP server for live peer sync, (7) managing network peers, (8) verifying remote peers, (9) generating weekly digests, (10) integrating MYR with an agent memory system, or (11) configuring auto-approval for verified peers. Triggers: "install MYR", "store a MYR", "what did we learn about", "weekly yield", "export yield", "import yield", "methodological yield", "MYR", "peer sync", "start MYR server", "verify peer", "announce to peer".
---

# MYR — Methodological Yield Reports

A pistis-native intelligence compounding system. Every meaningful OODA cycle (Observe, Orient, Decide, Act) produces yield — techniques, insights, falsifications, patterns. MYR captures it cryptographically signed so it compounds across sessions, agents, and nodes.

**Repo:** https://github.com/JordanGreenhall/myr-system

## Required Outputs

For every MYR operation, return:
1. Action performed
2. Artifact IDs affected
3. Verification result
4. Next recommended step

## Installation (New Node)

### One-step install (recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/JordanGreenhall/myr-system/main/install.sh | bash
```

This clones the repo, installs dependencies, generates your keypair, prompts for a node ID, runs the five-command ping test, and adds `MYR_HOME` to your shell. Node is operational when it completes.

If you already have the repo cloned:

```bash
bash install.sh
```

### Manual install

```bash
git clone https://github.com/JordanGreenhall/myr-system.git
cd myr-system
npm install
cp config.example.json config.json
```

Edit `config.json`:
- Set unique `node_id` (short, e.g. `n2`, `north-star`) — **must not be `n1`**
- Set `port` (default: 3719, choose any open port)
- Set `node_url` to your externally reachable address (Tailscale IP recommended — see Network section)
- Confirm paths and key locations are writable

Generate keys:

```bash
node scripts/myr-keygen.js
```

Set environment:

```bash
export MYR_HOME=/absolute/path/to/myr-system
```

## Node Identity

Every node must have a unique `node_id` and a `node_uuid`. These are set during keygen and enforced at runtime.

**All scripts refuse to run if `node_id` is still the default `"n1"`.** You will get an error with remediation steps and exit 1.

`myr-keygen` generates your keypair and writes `node_uuid` to `config.json` automatically. Verify your identity:

```bash
node $MYR_HOME/scripts/myr-identity.js
```

Output:
```
MYR Node Identity
─────────────────────────────────────────
  node_id:     n2
  node_uuid:   0c12b56f-0e44-44df-82a9-53d32dd0b1f3
  key:         SHA256:212a98c0e6f6b3c9…

  Fingerprint: n2 / 0c12b56f / SHA256:212a98c0e6f6b3c9…
─────────────────────────────────────────
```

## Verify Installation (Ping Test)

Run all five. All must succeed.

```bash
cd $MYR_HOME
node scripts/myr-store.js --intent "Installation test" --type technique \
  --question "Does MYR work on this node?" --evidence "Store succeeded" \
  --changes "MYR is operational" --tags "test"
node scripts/myr-search.js --query "installation test"
node scripts/myr-verify.js --queue
node scripts/myr-sign.js --all
node scripts/myr-export.js --all
```

If all five succeed, node is operational.

---

## HTTP Server (Live Peer Sync)

MYR includes an HTTP server for live peer-to-peer synchronization. Peers sync automatically on a schedule — no manual package exchange required.

### Start the server

```bash
cd $MYR_HOME
node server/index.js
```

Output:
```
MYR node server listening on port 3719
  Discovery: http://<your-ip>:3719/.well-known/myr-node
  Health:    http://<your-ip>:3719/myr/health
```

### Run as a persistent service (macOS launchd)

Create `~/Library/LaunchAgents/com.myr.server.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.myr.server</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/node</string>
        <string>/path/to/myr-system/server/index.js</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/path/to/myr-system</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>MYR_HOME</key>
        <string>/path/to/myr-system</string>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/path/to/myr-system/logs/server.log</string>
    <key>StandardErrorPath</key>
    <string>/path/to/myr-system/logs/server-error.log</string>
</dict>
</plist>
```

```bash
mkdir -p $MYR_HOME/logs
launchctl load ~/Library/LaunchAgents/com.myr.server.plist
```

Verify:
```bash
curl http://localhost:<port>/myr/health
```

### Server endpoints

| Endpoint | Auth | Purpose |
|----------|------|---------|
| `GET /.well-known/myr-node` | None | Node discovery (protocol version, public key, capabilities) |
| `GET /myr/health` | None | Health check (status, peer count, report count) |
| `GET /myr/reports` | Peer key | List shareable reports (supports `since`, `limit` params) |
| `GET /myr/reports/:signature` | Peer key | Fetch individual report |
| `POST /myr/peers/announce` | None | Peer announces itself for pairing |

### Network reachability

Peers must be able to reach each other's server. Options:

- **Tailscale (recommended):** Install Tailscale on both nodes, set `node_url` to your Tailscale IP (e.g. `http://100.x.x.x:3719`). Private, encrypted, no port forwarding needed.
- **VPN:** Any shared VPN works the same way.
- **Public internet:** Set `node_url` to your public IP/domain with port forwarding. Less recommended.

---

## Peer Management

The `bin/myr.js` CLI manages live peers.

### Add a peer by URL

```bash
node $MYR_HOME/bin/myr.js add-peer http://<peer-tailscale-ip>:<port>
```

This fetches the peer's discovery document, registers their public key, and sets trust to `pending`.

### Exchange fingerprints out-of-band (required)

Before approving any peer, verify their fingerprint through a separate channel (voice, Signal, in-person):

```bash
# Your fingerprint — share this with your peer
node $MYR_HOME/bin/myr.js fingerprint

# Peer's fingerprint — confirm this matches what they told you
node $MYR_HOME/bin/myr.js peer-fingerprint <peer-node-id>
```

**Do not approve a peer without confirming fingerprints out-of-band.** This is the trust anchor.

### Approve or reject

```bash
node $MYR_HOME/bin/myr.js approve-peer <node-id-or-url>
node $MYR_HOME/bin/myr.js reject-peer <node-id-or-url>
```

### List peers

```bash
node $MYR_HOME/bin/myr.js peers
```

### Manual sync (on demand)

```bash
node $MYR_HOME/bin/myr.js sync <peer-node-id>
```

Automatic sync runs every 15 minutes for all trusted peers once the server is running.

### Mark reports as shareable

Only reports explicitly marked `share_network=1` are served to peers. Mark your verified reports:

```sql
-- In your MYR database (db/myr.db)
BEGIN IMMEDIATE;
UPDATE myr_reports SET share_network=1
WHERE node_id='<your-node-id>' AND operator_rating >= 3 AND verified_at IS NOT NULL;
COMMIT;
```

---

## Connecting to an Existing Peer (Full Flow)

1. **Start your server** and confirm it's reachable at your `node_url`
2. **Get peer's URL** — their Tailscale IP and port
3. **Add them:** `node bin/myr.js add-peer <peer-url>`
4. **Exchange fingerprints out-of-band** — call, Signal, in-person
5. **Approve:** `node bin/myr.js approve-peer <peer-node-id>`
6. **Ask peer to approve you** — they run the same steps from their side
7. **Verify sync:** `node bin/myr.js sync <peer-node-id>` — should return reports
8. **Mark your reports shareable** (see above) so peers can pull from you

---

## Peer Verification (v1.2.0)

MYR v1.2.0 introduces in-band fingerprint verification during the announce flow. When a peer announces to your node, a 3-way check runs automatically:

1. The announced fingerprint matches the fingerprint computed from the announced public key.
2. The peer's discovery document is fetched from their URL.
3. The discovery document fingerprint matches both the announced and computed fingerprints.

Peers passing all three checks are marked `verified-pending-approval`. Peers failing any check are `rejected` with evidence stored for audit.

### Verify a remote peer (CLI)

```bash
node $MYR_HOME/bin/myr.js node verify --url <peer-url>
```

Returns verified status, operator name, fingerprint, and latency. Exit code 1 on failure.

### Announce to a peer

When adding a peer with `myr peer add --url <url>`, MYR fetches the peer's discovery document and sends an introduce request. In v1.2.0, the announce body includes `fingerprint`, `node_uuid`, and `protocol_version` fields for in-band verification.

### Auto-approve verified peers

Set `auto_approve_verified_peers: true` in your node config (`~/.myr/config.json` or `config.json`) to automatically trust peers that pass 3-way fingerprint verification:

```json
{
  "auto_approve_verified_peers": true,
  "auto_approve_min_protocol_version": "1.2.0"
}
```

When enabled:
- Peers announcing with protocol version ≥ `auto_approve_min_protocol_version` (default `1.2.0`) that pass 3-way verification are immediately trusted.
- A reciprocal announce is sent automatically so both sides can establish trust in a single round-trip.
- The `auto_approved` flag is recorded in the peer record for audit.

**Security note:** Only enable auto-approve on nodes where you trust the network environment. On untrusted networks, keep manual approval (`auto_approve_verified_peers: false`, the default) and verify fingerprints out-of-band.

---

## Capturing Yield

```bash
node $MYR_HOME/scripts/myr-store.js \
  --intent "What was being attempted" \
  --type insight \
  --question "The specific question resolved" \
  --evidence "Observable evidence supporting the answer" \
  --changes "What will be different next cycle" \
  --tags "domain1,domain2" \
  [--falsified "What was proven NOT to work"] \
  [--confidence 0.85] \
  [--agent agent-name]
```

Yield types:
- `technique` — reusable method that works
- `insight` — orientation-changing understanding
- `falsification` — proof something does not work (high value)
- `pattern` — recurring structure across cycles

## Searching Prior Yield

```bash
node $MYR_HOME/scripts/myr-search.js --query "topic" [--tags "domain"] [--type technique] [--limit 5]
```

Use before known-domain work, architecture decisions, and when asked "what do we know about X?"

## Verification and Rating Policy

- Rating scale is 1–5.
- Only designated operators may assign final ratings.
- A MYR is "network-eligible" only after at least 1 operator review with rating ≥ 3.
- Node join criterion: at least 10 MYRs, average operator rating ≥ 3.0 over the most recent 10 reviewed MYRs.

```bash
node $MYR_HOME/scripts/myr-verify.js --queue
node $MYR_HOME/scripts/myr-verify.js --id ID --rating 4 --notes "..."
```

## Weekly Digest

```bash
node $MYR_HOME/scripts/myr-weekly.js [--week 2026-02-17] [--output report.md]
```

## Manual Package Exchange (Alternative to Live Sync)

If live server sync is not available, export/import signed packages manually.

### Export

```bash
node $MYR_HOME/scripts/myr-export.js --all
```

Produces signed JSON in `$MYR_HOME/exports/`.

### Import

```bash
node $MYR_HOME/scripts/myr-import.js --file path.myr.json [--peer-key keys/peer.public.pem]
```

Import errors:
- `"You are importing your own artifacts"` — node_id and node_uuid match your node. Exit 2.
- `"Label collision between two different nodes"` — node_id matches but node_uuid differs. Peer must set a unique node_id and re-export. Exit 2.
- Key mismatch: import exits 3 with remediation. No silent key overwrite.

## Cross-Node Synthesis

```bash
node $MYR_HOME/scripts/myr-synthesize.js --tags "domain" --min-nodes 2
```

Identifies convergent findings, divergences, and unique contributions across nodes.

## Signing and Trust Requirements

- Every exported MYR bundle must include a detached signature and signer ID.
- Import must fail closed on signature verification failure.
- Never merge unsigned or unverifiable MYRs into trusted datasets.

## Memory-System Integration (Async)

- MYR capture must be fire-and-forget from the primary agent flow.
- Do not block user response on MYR persistence.
- On persistence failure, log the error and surface a non-fatal warning.

## ID Format

`{node_id}-{YYYYMMDD}-{seq}` — example: `n2-20260227-001`

## Architecture

For network protocol and scale roadmap, see:
`$MYR_HOME/docs/NETWORK-ARCHITECTURE.md`
