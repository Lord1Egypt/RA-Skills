# LCP/1.1 Protocol Specification

## Overview

Lobster Communication Protocol (LCP) version 1.1 is a lightweight, reliable messaging protocol designed for AI agent-to-agent communication over UDP. It provides message signing, acknowledgment-based reliability, and peer liveness detection.

## Design Goals

1. **Low latency**: UDP-based, no connection setup overhead
2. **Reliability**: Application-layer ACK with exponential backoff
3. **Security**: Ed25519 cryptographic message signing
4. **Simplicity**: Minimal wire format, JSON payloads
5. **Resilience**: Duplicate detection, heartbeat keep-alive, crash recovery

## Wire Format

Every LCP packet has a fixed 9-byte header followed by an optional payload:

```
Offset  Size  Field
0       4B    Magic Number: ASCII "LCP1" (0x4C435031)
4       4B    Sequence Number: uint32, big-endian, monotonically increasing
8       1B    Message Type: 0x01=DATA, 0x02=ACK, 0x03=HEARTBEAT
9+      var   Payload (JSON for DATA, empty for ACK/HEARTBEAT)
```

### Message Types

#### DATA (0x01)

Carries a JSON-encoded message. The receiver MUST:
1. Send an ACK with the same sequence number
2. Parse and verify the JSON payload
3. Check the Ed25519 signature
4. Check for duplicate message IDs
5. Store the message if valid and new

#### ACK (0x02)

Acknowledges receipt of a DATA or HEARTBEAT packet. Contains only the header (no payload). The sequence number matches the packet being acknowledged.

#### HEARTBEAT (0x03)

Keep-alive probe sent periodically. The receiver SHOULD respond with an ACK. Used to track peer liveness.

## Reliability

### Transmission

1. Sender assigns a unique sequence number
2. Sender transmits the packet
3. Sender waits for ACK up to `RETRY_BASE_MS * 2^attempt` milliseconds
4. If no ACK received, retransmit (up to MAX_RETRIES times)
5. If all retries exhausted, report delivery failure

### Duplicate Detection

Receivers maintain a set of seen message IDs (from the JSON `id` field). Messages with previously-seen IDs are silently dropped after sending an ACK. The seen-ID set is persisted to disk and trimmed to MAX_SEEN entries.

## Security

### Message Signing

Every DATA message includes a `security` block:

```json
{
  "security": {
    "algo": "ed25519",
    "pubkey": "<base64-encoded-public-key>",
    "signature": "<base64-encoded-signature>"
  }
}
```

**Signing process:**
1. Remove the `security` field from the message
2. Canonicalize: `JSON.dumps(msg, sort_keys=True, separators=(',', ':'))`
3. Sign the canonical bytes with the sender's Ed25519 private key
4. Attach the signature and public key in the `security` block

**Verification process:**
1. Extract and remove the `security` block
2. Canonicalize the remaining message (same method)
3. Verify the signature against the public key

### Key Management

Each node generates an Ed25519 keypair on first run. The 32-byte seed is stored locally. In production, consider a trust-on-first-use (TOFU) model or pre-shared public key exchange.

## Message Format (JSON Payload)

```json
{
  "id": "UUID v4",
  "from": "sender-agent-name",
  "to": "receiver-agent-name",
  "timestamp": "ISO-8601 with timezone",
  "type": "chat|task|result|ping|pong",
  "message": "human-readable content",
  "replyTo": "optional: ID of message being replied to",
  "security": { ... }
}
```

### Message Types

| Type | Purpose | Expected Response |
|------|---------|-------------------|
| `ping` | Connectivity test | `pong` |
| `pong` | Ping response | None |
| `chat` | General conversation | Optional `chat` reply |
| `task` | Task delegation | `result` with outcome |
| `result` | Task completion report | None |

## IPC Interface

The daemon exposes a local IPC interface for agent interaction:

| Command | Description | Response |
|---------|-------------|----------|
| `SEND` | Send a message to peer | `{ok, id}` |
| `CHECK` | List inbox messages | `{count, messages}` |
| `ACK` | Archive all inbox messages | `{archived}` |
| `STATUS` | Daemon and peer status | `{peer, peer_online, inbox_count, uptime}` |
| `PING` | Send a ping to peer | `{ok}` |

**macOS**: Unix domain socket at `/tmp/lcp.sock`
**Windows**: TCP socket at `127.0.0.1:9529`

## Configuration Defaults

```
LCP_PORT           = 9528
MAX_RETRIES        = 5
RETRY_BASE_MS      = 500
ACK_TIMEOUT_S      = 3.0
HEARTBEAT_INTERVAL = 30s
PEER_TIMEOUT       = 120s
MAX_SEEN_IDS       = 10000
```

## Future Considerations

- **Multi-peer**: Peer registry with per-peer state tracking
- **Encryption**: Add NaCl Box encryption for payload confidentiality
- **Chunking**: Fragment large messages across multiple DATA packets
- **NAT traversal**: STUN/TURN for peers without Tailscale
- **Group messaging**: Multicast or relay-based group channels
