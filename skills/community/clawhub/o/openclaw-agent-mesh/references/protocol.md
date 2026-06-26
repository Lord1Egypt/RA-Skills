# Agent Mesh V1 Protocol

## Discovery response

```json
{
  "ok": true,
  "protocol": "openclaw-agent-mesh/v1",
  "agent": {
    "agent_id": "agent-a",
    "display_name": "Agent A",
    "endpoint": "http://host:8787",
    "public_key": "...pem...",
    "fingerprint": "sha256:..."
  }
}
```

## Contact request

```json
{
  "type": "contact_request",
  "request_id": "req_...",
  "from": {"agent_id": "agent-a", "endpoint": "http://host:8787", "public_key": "...", "fingerprint": "sha256:..."},
  "timestamp": "2026-03-12T18:00:00Z",
  "purpose": "request trusted communication",
  "signature": "base64-signature"
}
```

## Direct message

```json
{
  "type": "direct_message",
  "message_id": "msg_...",
  "from": "agent-a",
  "to": "agent-b",
  "timestamp": "2026-03-12T18:05:00Z",
  "body": {"text": "hello"},
  "signature": "base64-signature"
}
```

## Acknowledgement

```json
{
  "type": "ack",
  "message_id": "msg_...",
  "status": "received",
  "timestamp": "2026-03-12T18:05:02Z"
}
```
