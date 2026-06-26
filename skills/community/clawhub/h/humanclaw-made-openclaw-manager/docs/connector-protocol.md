# Connector Protocol

External sources are normalized into a single inbound message shape before they touch the control plane.

```json
{
  "request_id": "req_...",
  "external_trigger_id": "ext_...",
  "source_type": "telegram",
  "source_thread_key": "telegram:12345",
  "source_message_id": "778899",
  "source_author_id": "agent_user",
  "source_author_name": "Agent User",
  "target_session_id": "sess_...",
  "message_type": "user_message",
  "content": "New inbound content",
  "attachments": [],
  "timestamp": "2026-03-17T10:00:00.000Z",
  "metadata": {}
}
```

Connector responsibilities:

- parse source-specific payloads
- derive a stable external thread key
- normalize author identity and message id
- preserve attachments and transport metadata
- resolve existing bindings in `connectors/bindings.json`
- update or create a `ThreadShadow`
- promote only when promotion rules require full session tracking

Implemented adapters:

- Telegram
- WeCom
- Email
- GitHub

Connector configs are stored locally in `connectors/configs.json`. Real secrets stay in local environment variables or private config files, not in git.

Connectors do not perform external work until you explicitly configure the relevant connector. Bootstrap networking remains separate and loopback-only.
