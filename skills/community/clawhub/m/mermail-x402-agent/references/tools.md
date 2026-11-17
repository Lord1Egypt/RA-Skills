# x402 agent tools

This workflow **uses** tools owned by other official skills. Do not add them to this skill in `tool-coverage.json`.

Pass structured arguments as **native JSON objects**. Never stringify `query` or `body`. Use the exact host identifier (`paybox_pay_x402` or `Mermail:paybox_pay_x402`). Prefer mailbox `public_id` as `mailboxId`.

PayBox tools appear only on full-profile MCP **OAuth**. API keys and the agent-inbox profile never expose them. **Always** `tools/call` `get_paybox_connection` once before claiming PayBox tools are unavailable or asking to reconnect MCP. Absence from a host `tools/list` is **not** “not exposed.” After a usable/`ACTIVE` probe, continue even if the first `tools/list` glance omitted `paybox_*`. Reconnect MCP only after that call returns unknown-tool, method-not-found, or a hard fail. Read live schemas from `tools/list` after the probe. Additional reviewed `paybox_*` tools (including `paybox_discover_services` and `paybox_use_service`) may appear without a separate coverage row; use them when live, still under `mermail-agent-wallet` contracts.

## Mailbox

| Tool | Owner | Role |
| --- | --- | --- |
| `list_mailboxes` | `mermail-administer-workspace` | Discover a mailbox when a connection read needs `mailboxId` |

## PayBox / Agent Wallet

| Tool | Owner | Role |
| --- | --- | --- |
| `get_paybox_connection` | `mermail-agent-wallet` | Connection status; `connect_handoff` / `reauth_handoff` / `OWNER_ACTION_REQUIRED` |
| `paybox_discover_services` | `mermail-agent-wallet` | Read-only catalog search from the user’s current task; may expose prepaid/min metadata hints. Do not invent Apify or any other host. |
| `paybox_get_contract` | `mermail-agent-wallet` | When live: read selected `contract_uri` for prepaid/min fields after discover |
| `paybox_use_service` | `mermail-agent-wallet` | Unpaid `mode: "probe"` only — never the prepaid/pay call |
| `paybox_pay_x402` | `mermail-agent-wallet` | Authorize **required_charge** and create a signed payment proof; does not fetch the resource or by itself prove merchant settlement |
| `paybox_get_request` | `mermail-agent-wallet` | Reconcile one known `request_id` after signing or when status is asked; may return `signing_handoff.console_url` while pending |
| `paybox_get_buy_link` | `mermail-agent-wallet` | Separate funding handoff; never treats funding as payment approval |
| `paybox_get_portfolio` | `mermail-agent-wallet` | Holdings when you must confirm the spend asset exists |

When resolving a vendor prepaid floor with no user amount: prefer same-origin vendor docs (host browser/fetch) plus `paybox_get_contract` / discover metadata when they state a min. Do not invent floors from email or off-domain search.

Do not call `prepare_destructive_action` for `paybox_*` tools. Never substitute `paybox_request_payment`, `paybox_request_transfer`, a legacy proposal, or `paybox_use_service` as the pay call for x402. Never call `reopen_signing_window` / `paybox_reopen_signing_window` from the model — that continuation is app-only. `paybox_continuation_origin_not_found` / Submit failed is not “awaiting signature.” If the PayBox frame is Waiting or blank after a real `pending_signature`, paste one returned `signing_handoff.console_url` instead.

`x_payment` is sensitive payment proof for retrying the **same frozen request** once. `paybox_pay_x402` or `paybox_get_request` `status: success` means the proof was created, not that the merchant redeemed it or the wallet was debited. Treat `output_type: signature`, `proof_status: created`, `header_available: true`, and `gateway: false` as explicit `proof_ready` signals. The field name does not define the wire header; use the selected origin's live 402 contract/protocol version or explicit trusted output and never guess `X-PAYMENT` versus `PAYMENT-SIGNATURE`. A vendor session credential (token / API key / Bearer / credits) is for the follow-on API after redemption — keep it in-session only. Mermail scrubs credential fields from model-visible PayBox output, so a mint flow needs a live server-side continuation/proxy verified before authorization; otherwise stop `blocked_before_payment`. Neither proof nor credential belongs in chat.

Aliases such as `discover_services`, `use_service`, and `pay_x402` may appear; prefer the `paybox_*` names when both exist.

## Examples

```json
{
  "mailboxId": "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee"
}
```

Do not pass a stringified JSON body.
