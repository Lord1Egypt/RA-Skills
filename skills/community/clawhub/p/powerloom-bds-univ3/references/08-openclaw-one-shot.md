# OpenClaw: pay-signup + whale cron (one-shot prompt)

Use this as a **single agent message** after installing the skill from ClawHub. It matches how the skill is meant to run: **bounded** `bds_mpp_snapshot_allTrades` via `scripts/whale-cron.mjs`. The skill does **not** use streaming trade tools.

---

## Copy-paste prompt

````
Install the skill "🦄 Powerloom Uniswap V3 timeseries data" (powerloom-bds-univ3) from ClawHub.
After install, run npm install in the skill directory.

**REQUIRED INPUTS — gather BOTH from me in chat BEFORE running `signup-pay.mjs` or creating any cron job. STOP and ask if either is missing. Do NOT proceed past this section with values unresolved. Asking me for any of these AFTER the cron job is created is a failure mode — re-ask BEFORE cron creation.**

a. **Payer wallet private key** — paste your EVM private key for the funded wallet that will pay 50 $POWER for the credit plan. **Use a burner wallet only** — never a wallet holding significant assets or with extensive transaction history. This key is consumed by `node scripts/signup-pay.mjs` and stored in OpenClaw env as `POWERLOOM_EVM_PRIVATE_KEY`.

b. **Telegram alerts** — ask explicitly: "Do you want Telegram alerts for whale swaps? If yes, paste your `POWERLOOM_TELEGRAM_BOT_TOKEN` and `POWERLOOM_TELEGRAM_CHAT_ID`. If no, type 'skip' and alerts will print to stdout only."
   - If I give you both tokens → use them in the cron env (step 5 below).
   - If I explicitly say "skip" / "no Telegram" / "stdout only" → proceed without TG envs and tell me clearly in the final cron summary that alerts will only print to stdout (the cron `--no-deliver` flag means OpenClaw's chat won't see them either).
   - Do NOT silently default to "stdout is fine." Either both TG values, or an explicit opt-out.
   - Do NOT look up TG credentials from any OpenClaw config source (`channels.telegram`, `openclaw.json`, etc.) — only use what I paste in this conversation.

Once (a) and (b) are resolved in chat, proceed with the steps below.

Then set up pay-signup and a whale radar cron. Details:

1. PLAN: launch_10_pl_power_cgt (POWER native on chain 7869, rpc-v2.powerloom.network)
2. Pay-signup using `scripts/signup-pay.mjs` with the private key from input (a):
   - **Recommended:** run `node scripts/signup-pay.mjs --dry-run` first — prints quote summary (recipient, amount_atomic, chain, payment_kind) to stderr; paste into chat so I can confirm values against metering UI / `/credits/plans`.
   - **Broadcast (non-interactive):** run `node scripts/signup-pay.mjs --yes` as a **one-off shell command** after review — **do not** persist `--yes` or any confirmation bypass inside OpenClaw long-lived skill env (`skills.entries.*.env`). CI operators may instead use `POWERLOOM_SIGNUP_PAY_CONFIRM=yes` for a single invocation; avoid leaving that variable set in autonomous sessions.
   - **TTY:** omit `--yes`; the script prompts `CONFIRM` interactively.
   Non-interactive shells refuse to broadcast without `--yes` / `POWERLOOM_SIGNUP_PAY_CONFIRM=yes` — this is intentional broadcast protection.
   `signup-pay.mjs` uses `quote.payment_kind`: `native_value` → `sendTransaction({ value })`; `erc20` → `token.transfer()`.
3. After signup, set the `sk_live_...` API key and all six env vars in OpenClaw under
   `skills.entries.powerloom-bds-univ3.env.*`:
   `POWERLOOM_EVM_PRIVATE_KEY` (from input a), `POWERLOOM_EVM_RPC_URL`, `POWERLOOM_EVM_CHAIN_ID`, `POWERLOOM_PLAN_ID`, `POWERLOOM_TOKEN_SYMBOL`, `POWERLOOM_API_KEY` (from `signup-pay.mjs` claim output).
   Plus, if input (b) yielded values: `POWERLOOM_TELEGRAM_BOT_TOKEN`, `POWERLOOM_TELEGRAM_CHAT_ID`.
   If the schema expects strings, pass `POWERLOOM_EVM_CHAIN_ID` as a quoted string (e.g. `"7869"`).
4. `scripts/whale-cron.mjs` should:
   - Use `lib/mcp.mjs` `callTool()` for all MCP calls (SSE handshake, not raw HTTP).
   - Use `lib/trade-utils.mjs` `flattenAllTradesFromSnapshot()` to parse the snapshot.
   - Response shape: `result.data.tradeData` = `{ poolAddr: { trades: [...] } }`.
   - Resolve pool token names with `bds_mpp_pool_pool_address_metadata` per unknown pool;
     cache in `.powerloom/pool-metadata-cache.json` (override with `WHALE_CRON_POOL_CACHE`).
   - Verification: `result.data.verification` = `{ cid, epochId, projectId }` — surface in alerts (e.g. ✅).
   - Telegram: `parse_mode: MarkdownV2` with full escaping, or plain-text fallback.
   - If the script is missing or broken, rebuild using the skill’s `lib/*` helpers only.
5. Create an OpenClaw cron job — **only after** REQUIRED INPUTS (a) and (b) above are fully resolved in chat AND `signup-pay.mjs` has produced the API key:
   - Name: e.g. "Whale Radar"
   - Schedule: e.g. every 15s (`--every 15s` with `openclaw cron add`)
   - Timeout: 90s (`--timeout 90000`)
   - Session: isolated (`--session isolated`)
   - Flags: `--no-deliver`, `--light-context`
   - Message: a shell command that `cd`s to the skill dir, sets env inline, then runs `node scripts/whale-cron.mjs`. Required env in the cron message:
     - `POWERLOOM_API_KEY=<value from signup-pay.mjs claim output>`
     - `POWERLOOM_BDS_MCP_CALL_TIMEOUT_MS=120000`
     - `WHALE_CRON_THRESHOLD=10000` (default; only override if I asked for a different threshold)
   - Telegram env in the cron message — **only** if input (b) yielded both values:
     - `POWERLOOM_TELEGRAM_BOT_TOKEN=<value from input (b)>`
     - `POWERLOOM_TELEGRAM_CHAT_ID=<value from input (b)>`
   - Do NOT consult OpenClaw `channels.telegram`, `openclaw.json`, or any other config source for Telegram credentials — only use what I pasted in chat for input (b).
6. Before the first run: `rm -f .powerloom/whale-cron-state.json` if you need a clean epoch cursor.
   Keep `.powerloom/pool-metadata-cache.json` across reinstalls unless debugging metadata.
7. Set WHALE_CRON_STATE_FILE and WHALE_CRON_POOL_CACHE to paths outside the skill directory (e.g. in the workspace root) so they survive openclaw skills install --force.

Constraints:
- **Pay-signup broadcast:** run `node scripts/signup-pay.mjs --dry-run` first unless I explicitly waive dry-run in chat; paste stderr quote summary into chat for my review; then run **`node scripts/signup-pay.mjs --yes` once** as an ephemeral shell invocation (not saved in OpenClaw skill env). CI may use `POWERLOOM_SIGNUP_PAY_CONFIRM=yes` for a single job — do not leave confirmation bypass variables persisted alongside wallet keys. TTY sessions type `CONFIRM` instead.
- **Telegram credentials must be gathered from me in chat (or explicit opt-out received) BEFORE the cron job is created.** Asking me for `POWERLOOM_TELEGRAM_BOT_TOKEN` / `POWERLOOM_TELEGRAM_CHAT_ID` after running `openclaw cron add` and seeing the cron tick (with stdout-only alerts) is a known failure mode — fail the run and re-ask before cron creation.
- Do NOT use OpenClaw config (`channels.telegram`, `openclaw.json`, etc.) as a fallback Telegram source — chat input only.
- Use `bds_mpp_snapshot_allTrades` only (bounded batches). Do not add streaming trade tools.
- Do NOT run the tracker as a background process — use OpenClaw cron only.
- Do NOT show "???" for unknown tokens — resolve via the metadata tool or show the address.
````

---

## Verification provenance (cron script + one-shot)

**In `scripts/whale-cron.mjs` (already implemented):** each `bds_mpp_snapshot_allTrades` result carries `data.verification` (`cid`, `epochId`, `projectId`). The script reads that object once per poll and appends a **“Verified on-chain”** block (CID, epoch, project) to each formatted alert in `formatAlert` — it is not optional glue you add in the OpenClaw message; the one-shot above assumes this behavior.

**Independent check:** the MCP tool `verify_data_provenance` can confirm commitments using the same `cid` / `epoch_id` / `project_id` — see **`references/03-verification.md`** and the **Verify** row in `SKILL.md` (data table).

---

## Related files in this skill

| Item | Location |
|------|----------|
| Cron entrypoint (incl. verification in alerts) | `scripts/whale-cron.mjs` |
| Pay-signup | `scripts/signup-pay.mjs` |
| MCP + trade helpers | `lib/mcp.mjs`, `lib/trade-utils.mjs`, `lib/state.mjs` |
| On-chain verification details | `references/03-verification.md` |
| Integrator rules | `SKILL.md` → **Hosts & integrators** |

See also `references/01-quickstart.md` and `references/06-troubleshooting.md`.
