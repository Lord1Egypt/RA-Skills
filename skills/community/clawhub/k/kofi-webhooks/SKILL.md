---
name: kofi-webhooks
description: Deploy and activate a Ko-fi HTTPS webhook receiver, verify live test deliveries, and operate payment tracking with summaries and exports. Use for Ko-fi webhook setup, troubleshooting, and received-payment reporting, not general account editing or publishing.
---

# Ko-fi Webhooks

Ko-fi's documented API sends payment notifications to a receiver. It is not a REST account-management API. Do not invent endpoints for listing historical payments, editing products, posting content, refunds, or membership cancellation. For those requests, explain the narrow API limitation and use a separately authorized web workflow if available. Local history starts with received events, not the account's lifetime sales.

## Documentation

Read [references/webhooks.md](references/webhooks.md) for delivery semantics, event fields, source links, and scope. The supplied settings page is <https://ko-fi.com/manage/webhooks?src=sidemenu>. It may require a logged-in browser or block direct fetches; the official help article is accessible through its Zendesk JSON endpoint listed in the reference.

## Local tools

For an existing deployment, obtain the configured host and production database from the user's deployment configuration or notes. Run reports where that database lives; do not assume a local database contains live account history. Re-check current service state before changing an existing installation.

Resolve `scripts/kofi_webhooks.py` relative to this skill directory and use its absolute path. Python 3.10+ standard library only. The database defaults to `kofi-webhooks/events.sqlite3` under the user's data directory (`LOCALAPPDATA` on Windows; `XDG_DATA_HOME` or `~/.local/share` elsewhere). Override with global `--db PATH` or `KOFI_DB`. Keep tokens, databases, and supporter exports outside the skill/repository.

Commands (replace `<script>` with the resolved absolute script path):

```sh
python <script> --help
python <script> --db <private-database-path> serve --token-file <private-token-file>
python <script> list --limit 20
python <script> summary
python <script> export --output <private-new-export-path>
```

`serve` also accepts `KOFI_VERIFICATION_TOKEN` instead of `--token-file`. Use the verification token shown in Ko-fi's webhook settings, not a presumed OAuth/API bearer token. Do not print the token. A token file contains only the token. Restart the receiver after token rotation.

The listener defaults to `127.0.0.1:8787`. Routes:

- `POST /kofi`: URL-encoded form field `data` containing JSON; verifies the token and commits to SQLite before acknowledging with HTTP 200. Repeated `message_id` values return 200 without adding another event.
- `GET /healthz`: listener health only, never evidence that Ko-fi deliveries work.
- No payment-data read API is exposed over HTTP. Use the local CLI.

`list` and default `export` omit names, emails, messages, shipping and transaction links. `export --include-private` includes the full stored payload except the verification token. Aggregate summaries use exact decimal arithmetic and keep currencies separate; they are gross received-event totals, not net revenue or proof of current membership. Test events are not reliably identifiable from payload fields: use a separate test database and do not mix them into real totals.

## Connect when requested

Read [references/deployment.md](references/deployment.md) for the Linux/Nginx/systemd workflow: render configurable templates, prepare privately, deploy within authorization, test HTTPS against an isolated database, confirm Ko-fi-originated receipt, then activate production. It includes token transport, verification gates, recovery, and existing-server reporting commands. Other hosts can run the receiver directly behind their own HTTPS proxy; systemd is not a receiver dependency.

Creation or editing of the skill does not authorize a live deployment or account changes. Follow existing session authorization; do not ask again for steps already approved. When approval is still needed for a public endpoint/always-on service, first prepare concrete reviewable files and name the proposed endpoint and service. No DNS, firewall, paid resources, or unrelated configuration changes are implied.

If the user reports saving settings, check the receiver before asking for another action: a test may already have arrived. If it has not, request Ko-fi's test-payment action specifically, not a real purchase. Never equate local tests, a health check, or saving a URL with live Ko-fi delivery.

Report separately: local tests, external HTTPS verification, Ko-fi-originated receipt, production/test database selection, and startup persistence. An active production receiver should not be reset to an empty database on later uses of the skill.

Downstream notifications, content delivery, emails and other external actions require the user's authorization for that workflow. This helper only records events; it never sends messages or fulfills orders. If automation is added, use a durable job/outbox with its own idempotency and retry tracking; do not run side effects inside the webhook request before acknowledging it.

## Verify changes

Run `python -B scripts/test_kofi_webhooks.py` after modifying the receiver and `python -B scripts/test_render_deployment.py` after changing deployment rendering. Tests use temporary directories and loopback HTTP with synthetic data; no live account or public listener is needed. Publishing this skill requires no credentials: include only its instructions, references, templates, and source/tests, not local deployment receipts, compiled Python caches, or private state.
