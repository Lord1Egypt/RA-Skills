# Agent Wallet tool map

These tools appear only on Mermail MCP **OAuth** full-profile sessions. API-key catalogs and the agent-inbox profile never include them. Current workspace members can use `get_paybox_connection`, `get_paybox_invocation`, and model-visible live `paybox_*` through the workspace owner's active connection. Connect/reauthorize behavior and legacy Agent Wallet compatibility tools (`get_agent_wallet`, legacy credentials/portfolio/request, and proposal submit/reject flows) remain owner-only. Legacy `wallet:read` / `wallet:transact` scope strings are compatibility-only and are not used for tool visibility. Always call `get_paybox_connection` once (`tools/call`) before claiming tools unavailable or asking to reconnect MCP; absence from a host `tools/list` is **not** “not exposed.” After a usable/`ACTIVE` probe, continue even if the first `tools/list` glance omitted `paybox_*`. Reconnect MCP only after that call returns unknown-tool, method-not-found, or a hard fail. Read live schemas from MCP `tools/list` after the probe.

**Do not call `prepare_destructive_action` for `paybox_*` or legacy Agent Wallet submit/reject tools.** PayBox owns transaction policy, signing, and approval. `prepare_destructive_action` remains for non-PayBox Mermail destructive tools (mailbox/workspace admin, etc.). Core OAuth grant is `mcp:tools`.

## Read

- `get_paybox_connection`: lightweight PayBox status for one mailbox. For the owner, returns `connect_handoff.console_url` when not connected or `reauth_handoff.console_url` when reauth is required. For a member whose owner's connection needs action, returns `OWNER_ACTION_REQUIRED` with no handoff; ask the owner to repair PayBox in Mermail. Never send users to Claude/ChatGPT/Codex connector settings.
- `get_agent_wallet`: connection, credentials summary, portfolio, and proposal statuses for one mailbox. May include `connect_handoff` / `reauth_handoff` / `funding_handoff`. `connection.status` of `PAYBOX_UNAVAILABLE` with an empty portfolio means PayBox did not answer that read, not a disconnect.
- `list_agent_wallet_credentials`: delegated wallet credentials only; secrets, cards, and raw signing credentials are never returned.
- `get_agent_wallet_portfolio`: portfolio view for the connected PayBox workspace.
- `paybox_get_portfolio`: direct PayBox holdings when that tool is registered. Asset `token` addresses are returned in the clear, so read the transfer asset from here instead of guessing an address.
- `paybox_get_request`: authoritative provider business status for one known transfer, swap, or x402 `request_id`; use it to distinguish pending from terminal settlement. May include an invocation-scoped `signing_handoff.console_url` while pending signature.
- `paybox_list_credentials`: discover chain eligibility, `credential_id`, and `approval_mode` before a financial write. Preserve an explicit selection; prefer only one eligible autonomous wallet when choosing for the user. Never treat an unknown mode or missing chain metadata as autonomous or compatible.
- `get_agent_wallet_request`: poll a known Mermail provider request id; never creates or retries a transfer.
- `get_paybox_invocation`: read safe MCP invocation/audit state for one OAuth-grant invocation. This can show that the proxied tool call completed while its provider transfer, swap, or x402 request remains pending; never use it as proof of settlement or as the sole reason to block a distinct new action. Approval URLs and signing plans are never returned.

## Write

### Primary (in-app parity)

- `paybox_request_transfer`: **default for every new transfer** — Circle USDC, native ETH/SOL, and any other reviewed catalog token. Pass arguments exactly as the live schema requires. Do **not** call `prepare_destructive_action`. May be absent from `tools/list` even when other `paybox_*` tools are live; if so, say unavailable — do **not** fall back to creating a USDC proposal.
- `paybox_request_swap`: **default for token A → token B swaps**. Read the live schema (commonly `credential_id`, `src_chain`, `src_token`, `dst_token`, `amount`). Do not substitute a transfer or USDC proposal. Do **not** call `prepare_destructive_action`.
- `paybox_pay_x402`: **only for an explicitly selected x402 paid resource/action** when this model-visible tool appears in live `tools/list`. Read its live description/schema. Call once; never call it again to resume signing. After terminal success, classify paid output: `x_payment` is proof for retrying the **same** 402 URL once; a vendor session credential stays in-session only and must not replay a settled mint URL. Neither is authority for another payment. Do not substitute `paybox_request_payment`, a transfer, or a proposal; those are different operations. Do **not** call `prepare_destructive_action`.

### Legacy proposals (only when user explicitly manages an existing proposal)

- `create_agent_wallet_transfer_proposal`: create a local USDC proposal for review (`mailboxId`, `chain`, `amount`, `destination`). USDC only. Reuses a matching `PENDING_REVIEW` proposal. Does not submit or sign. **Do not use for a normal “send money” request.**
- `submit_agent_wallet_transfer`: submit a reviewed proposal with `{ proposalId, version }` only. Do **not** call `prepare_destructive_action`. If pending, prefer PayBox MCP App UI when present; else paste `signing_handoff.console_url` when present. Pending is not success. Do not retry after `wallet_proposal_already_handled` / `wallet_proposal_not_pending` / `wallet_paybox_credential_unavailable`.
- `reject_agent_wallet_transfer_proposal`: cancel one `PENDING_REVIEW` proposal (`proposalId`, `version`). Do **not** call `prepare_destructive_action`. Does not cancel submitted or PayBox-parked transfers.

## Related PayBox direct tools

When PayBox is connected, additional reviewed `paybox_*` tools may appear for the same OAuth grant. Mermail does not add Mermail confirmation tokens to those writes.

These live tools execute with the owner's PayBox connection but retain the invoking member as the audited actor. Do not present connection ownership as permission to broaden the member's request, and do not expose app-only upstream aliases that `tools/list` hides from the model.

- **Send (including USDC):** use `paybox_request_transfer` with live-schema args. Tools may declare `_meta.ui.resourceUri` / `ui/resourceUri` for a PayBox MCP App. When status is `pending_signature` / `pending_approval`, prefer an in-chat frame with usable signing controls. If the frame is absent or remains on “Waiting,” paste one returned `signing_handoff.console_url`. Never expect a pasteable signing plan or approval URL.
- **Swap token A → token B:** use `paybox_request_swap` with live-schema arguments. Prefer a PayBox MCP App with usable signing controls on `pending_signature`; otherwise present one returned signing handoff and stop the model turn. Do not auto-poll; poll once only if the user asks or confirms finish. Never claim success merely because the swap was prepared or invent a console URL.
- **x402 paid service:** exploration is read-only. Before `paybox_pay_x402`, require a user-selected service/origin, resource/action, and maximum spend; when the user omitted an amount, resolve the vendor prepaid floor from same-origin docs or `paybox_get_contract` / discover metadata, then set **required_charge = max(live quote, vendor prepaid floor)**. Preview quote, floor (cite source), required_charge, and cap. Never submit only the live quote when a resolved vendor prepaid floor is higher. Funding is separate and never authorizes payment. Call `paybox_pay_x402` once (not `paybox_use_service`) and stop on pending. `paybox_continuation_origin_not_found` / Submit failed is not “awaiting signature.” If the PayBox frame is Waiting or blank after real `pending_signature`, paste one returned `signing_handoff.console_url`; never call `reopen_signing_window` from the model. After terminal success, classify paid output: keep `x_payment` and vendor session credentials out of chat; retry the same 402 URL with `x_payment` only for a direct resource; never replay a settled mint/pay URL.
- Poll known transfer, swap, or x402 provider state with `paybox_get_request` **once** after the user finishes signing, asks for status, or explicitly requests a new wallet action while an old provider request is pending in chat. Use `get_paybox_invocation` only for MCP invocation/audit state. Never poll by starting another write; after reconciliation, a clearly distinct new action uses a new request ID and its own single write.
- `show_paybox_signing` — external MCP signing display. Call it only for an actual `pending_signature`, with the original returned `signing_handoff.invocation_id`, then end the response so the host can render the signer. Do not call it for `pending_execution`, `pending_confirmation`, or `pending_settlement`.

## Native USDC bridge tools

- `list_bridge_routes` — read supported native USDC source/destination routes.
- `prepare_bridge` — prepare one exact quote with `credentialId`, `sourceChain`, `destinationChain`, `recipient`, decimal `amount` (at most six fractional digits), and stable `idempotencyKey`. This does not move funds and does not replace owner quote approval.
- `get_bridge_status` — read the original transfer using its returned `quoteId`. Only confirmed destination delivery is success; do not repeat `prepare_bridge` to poll or recover.

Buy / checkout / approval / signing-plan URLs from tools such as `paybox_get_buy_link` are redacted for the model. When the live buy-link tool is visible, call it once and use its MCP App or returned first-party `funding_handoff.console_url`; owners may also use `get_agent_wallet` → `funding_handoff.console_url` (Mermail deep link with `fund=1`). If a handoff needs a mailbox, resolve an explicit `mailboxId` instead of guessing. Signing handoffs are different: use only the returned invocation-scoped URL and never construct one. See [SKILL.md](../SKILL.md).

For exact sequencing, read [workflows.md](workflows.md). Keep this file as the live tool map; do not infer workflow authority from tool availability alone.
