# Mail Reference

## Listing

```
python scripts/mail_fetch.py --folder Inbox --top 10 --unread
```

- `--filter` accepts OData expressions (`contains(subject,'Status')`).
- `--id <messageId>` fetches a specific message.
- `--include-body` returns full body content (HTML + text).
- `--mark-read` and `--move-to <folderId>` act on the message loaded with `--id`.

## Sending

```
python scripts/mail_send.py \
  --to user@example.com \
  --subject "Follow-up" \
  --body-file drafts/reply.html --html \
  --cc teammate@example.com \
  --attachment docs/proposal.pdf
```

- `saveToSentItems` is `True` by default. Use `--no-save-copy` to disable.
- Attachments are sent as `fileAttachment` and are limited on this endpoint; for large files, implement upload session flow.

## Useful folder IDs

List folders with:
```
curl -H "Authorization: Bearer <ACCESS_TOKEN>" \
  https://graph.microsoft.com/v1.0/me/mailFolders
```
Or query a known folder with `mail_fetch.py --folder SentItems`.

## Push mode (no inbox polling)

### Start webhook adapter

```
python scripts/mail_webhook_adapter.py serve \
  --host 0.0.0.0 \
  --port 8789 \
  --path /graph/mail \
  --client-state "$GRAPH_WEBHOOK_CLIENT_STATE"
```

### Create Graph subscription

```
python scripts/mail_subscriptions.py create \
  --notification-url "https://graph-hook.example.com/graph/mail" \
  --client-state "$GRAPH_WEBHOOK_CLIENT_STATE" \
  --minutes 4200
```

- Default resource is `me/messages` (broader and more resilient to routing/folder variations).
- You can still scope manually with `--resource`, but `me/mailFolders('Inbox')/messages` may miss some real deliveries depending on mailbox behavior.

### Process notifications asynchronously

```
python scripts/mail_webhook_worker.py loop \
  --session-key "$OPENCLAW_SESSION_KEY" \
  --hook-url "$OPENCLAW_HOOK_URL" \
  --hook-token "$OPENCLAW_HOOK_TOKEN"
```

- Adapter responds to Graph validation (`validationToken`) and enqueues compact events.
- Worker performs dedupe by `subscriptionId/messageId/changeType`.
- Worker default mode posts a `wake` signal to OpenClaw `/hooks/wake` (`mode=now`) so the inbox is processed in the next heartbeat cycle.
- Optional advanced mode: `--hook-action agent` to fetch full mail via Graph and post a rich payload to `/hooks/agent`.
- In production, values are typically loaded from `/etc/default/graph-mail-webhook` created by setup scripts; `OPENCLAW_SESSION_KEY` is optional (default `hook:graph-mail`).
- Renew subscriptions before expiration:

```
python scripts/mail_subscriptions.py renew --id "<subscription-id>" --minutes 4200
```

### Quick validation checklist (post-subscription)

- Confirm adapter receives real deliveries: `journalctl -u graph-mail-webhook-adapter --since "15 minutes ago" | rg 'POST /graph/mail HTTP/1.1" 202'`
- Confirm queue receives events: `wc -l state/mail_webhook_queue.jsonl`
- Confirm worker processes items: `tail -n 80 state/graph_ops.log | rg 'mail_webhook_processed|mail_webhook_drop_max_retries'`

See full setup, checklists, and troubleshooting in:
`references/mail_webhook_adapter.md`.
