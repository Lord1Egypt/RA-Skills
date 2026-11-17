# Workspace webhooks

Webhooks are workspace-admin resources that deliver selected email content to an external destination. Resolve the credential-bound workspace first. Use `list_webhooks`, `get_webhook`, and `list_webhook_deliveries` for discovery and status; a status check never needs a test, retry, update, or secret rotation.

Before `create_webhook` or `update_webhook`, show the exact event set, enabled state, destination host, and whether an Authorization value will be stored. Treat the full destination URL and Authorization value as write-only even when a read omits or redacts them. Do not reconstruct either value from memory. A create returns the signing secret only once; keep it in the secure tool result and do not repeat it in chat, logs, drafts, or email.

`create_webhook`, `update_webhook`, `delete_webhook`, `test_webhook`, `retry_webhook_delivery`, and `rotate_webhook_secret` require explicit approval and a matching single-use `prepare_destructive_action` token for the exact arguments. A test sends an event to the configured external destination. A retry re-delivers one exact existing delivery. Secret rotation invalidates the previous secret and returns the replacement only once.

Supply an `idempotencyKey` for create, test, and retry. If a response times out or is unclear, keep the same key and identical arguments, inspect webhook or delivery state, and do not create a new key or broaden the request. Never test, retry, or rotate as a substitute for a read. Report success only from an authoritative tool result or a matching read; otherwise report `unverified` with the original webhook, delivery, and idempotency identities retained.
