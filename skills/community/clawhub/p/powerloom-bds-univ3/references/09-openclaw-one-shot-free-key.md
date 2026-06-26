# OpenClaw: free-key whale cron (one-shot prompt)

Use this as a **single agent message** after running `bds-agent signup` to get a free `sk_live_...` API key (browser device flow, 2 free credits, no wallet). The skill itself only needs **`POWERLOOM_API_KEY`** at runtime — `whale-cron.mjs` dispatches alerts via the hosted MCP server using that key alone.

For the wallet-funded variant (autonomous on-chain pay-signup for a 10-credit plan in the same prompt), see [`references/08-openclaw-one-shot.md`](./08-openclaw-one-shot.md).

---

## Copy-paste prompt

````
Install the skill "🦄 Powerloom Uniswap V3 timeseries data" (powerloom-bds-univ3) from ClawHub.
After install, run npm install in the skill directory.

I already have a Powerloom API key (sk_live_...) from `bds-agent signup` — 2 free credits, no wallet needed. Use that key directly. Do NOT run `scripts/signup-pay.mjs`. Do NOT ask for a private key, RPC URL, plan id, chain id, or token symbol.

**REQUIRED INPUTS — gather BOTH from me in chat BEFORE you install the skill, wire any env, or create any cron job. STOP and ask if either is missing. Do NOT proceed to step 1 below until both are resolved. Asking me for any of these AFTER creating the cron is a failure mode — re-ask BEFORE cron creation.**

a. **Powerloom API key** — paste your `sk_live_...` from `bds-agent signup`. If you don't have one yet, run `bds-agent signup` first (free, 2 credits, browser device flow) and come back. Do not invent or guess a key.

b. **Telegram alerts** — ask explicitly: "Do you want Telegram alerts for whale swaps? If yes, paste your `POWERLOOM_TELEGRAM_BOT_TOKEN` and `POWERLOOM_TELEGRAM_CHAT_ID`. If no, type 'skip' and alerts will print to stdout only."
   - If I give you both tokens → use them in the cron env (steps 1 and 4 below).
   - If I explicitly say "skip" / "no Telegram" / "stdout only" → proceed without TG envs and tell me clearly in the final cron summary that alerts will only print to stdout (the cron `--no-deliver` flag means OpenClaw's chat won't see them either).
   - Do NOT silently default to "stdout is fine." Either both TG values, or an explicit opt-out.
   - Do NOT look up TG credentials from any OpenClaw config source (`channels.telegram`, `openclaw.json`, etc.) — only use what I paste in this conversation.

Once (a) and (b) are resolved in chat, proceed with the steps below.

Set up a whale radar cron with the existing key. Details:

1. Set the gathered envs in OpenClaw under `skills.entries.powerloom-bds-univ3.env.*`:
   - `POWERLOOM_API_KEY` — required, from input (a).
   - `POWERLOOM_TELEGRAM_BOT_TOKEN`, `POWERLOOM_TELEGRAM_CHAT_ID` — set both **only** if I gave you values in input (b). If I opted out, leave both unset; `whale-cron.mjs` prints alerts to stdout in that case (still includes the verification block).

2. Pre-flight: `node scripts/ensure-credits.mjs` to confirm the key is valid and balance is non-zero (free signup grants 2 credits).

3. `scripts/whale-cron.mjs` should:
   - Use `lib/mcp.mjs` `callTool()` for all MCP calls (SSE handshake, not raw HTTP).
   - Use `lib/trade-utils.mjs` `flattenAllTradesFromSnapshot()` to parse the snapshot.
   - Response shape: `result.data.tradeData` = `{ poolAddr: { trades: [...] } }`.
   - Resolve pool token names with `bds_mpp_pool_pool_address_metadata` per unknown pool;
     cache in `.powerloom/pool-metadata-cache.json` (override with `WHALE_CRON_POOL_CACHE`).
   - Verification: `result.data.verification` = `{ cid, epochId, projectId }` — surface in alerts (e.g. ✅).
   - Telegram: `parse_mode: MarkdownV2` with full escaping, or plain-text fallback.
   - If the script is missing or broken, rebuild using the skill’s `lib/*` helpers only.

4. Create an OpenClaw cron job — **only after** REQUIRED INPUTS (a) and (b) above are fully resolved in chat:
   - Name: e.g. "Whale Radar"
   - Schedule: e.g. every 15s (`--every 15s` with `openclaw cron add`)
   - Timeout: 90s (`--timeout 90000`)
   - Session: isolated (`--session isolated`)
   - Flags: `--no-deliver`, `--light-context`
   - Message: a shell command that `cd`s to the skill dir, sets env inline, then runs `node scripts/whale-cron.mjs`. Required env in the cron message:
     - `POWERLOOM_API_KEY=<value from input (a)>`
     - `POWERLOOM_BDS_MCP_CALL_TIMEOUT_MS=120000`
     - `WHALE_CRON_THRESHOLD=10000` (default; only override if I asked for a different threshold)
   - Telegram env in the cron message — **only** if input (b) yielded both values:
     - `POWERLOOM_TELEGRAM_BOT_TOKEN=<value from input (b)>`
     - `POWERLOOM_TELEGRAM_CHAT_ID=<value from input (b)>`
   - Do NOT consult OpenClaw `channels.telegram`, `openclaw.json`, or any other config source for Telegram credentials — only use what I pasted in chat for input (b).

5. Before the first run: `rm -f .powerloom/whale-cron-state.json` if you need a clean epoch cursor.
   Keep `.powerloom/pool-metadata-cache.json` across reinstalls unless debugging metadata.

6. Set WHALE_CRON_STATE_FILE and WHALE_CRON_POOL_CACHE to paths outside the skill directory (e.g. in the workspace root) so they survive `openclaw skills install --force`.

Constraints:
- This flow uses an **existing** `sk_live_...` key only. Do NOT initiate any on-chain payment, and do NOT prompt for wallet credentials.
- **Telegram credentials must be gathered from me in chat (or explicit opt-out received) BEFORE the cron job is created.** Asking me for `POWERLOOM_TELEGRAM_BOT_TOKEN` / `POWERLOOM_TELEGRAM_CHAT_ID` after running `openclaw cron add` and seeing the cron tick (with stdout-only alerts) is a known failure mode — fail the run and re-ask before cron creation.
- Do NOT use OpenClaw config (`channels.telegram`, `openclaw.json`, etc.) as a fallback Telegram source — chat input only.
- If the user later wants more credits, point them at `references/08-openclaw-one-shot.md` (wallet-funded pay-signup variant) or `node scripts/credits-topup.mjs` against the same key.
- Use `bds_mpp_snapshot_allTrades` only (bounded batches). Do not add streaming trade tools.
- Do NOT run the tracker as a background process — use OpenClaw cron only.
- Do NOT show "???" for unknown tokens — resolve via the metadata tool or show the address.
````

---

## Why this works without a wallet

`scripts/whale-cron.mjs` only consumes `POWERLOOM_API_KEY` (via `lib/mcp.mjs`) plus the optional Telegram envs (`lib/powerloom-env.mjs` `telegramBotToken()` / `telegramChatId()`). The wallet/plan env getters in `lib/powerloom-env.mjs` are **only** read by `scripts/signup-pay.mjs` and `scripts/credits-topup.mjs` — both of which this prompt explicitly skips. The skill's `metadata.openclaw.requires.env` schema in `SKILL.md` lists wallet vars as **optional** (`optional_env`) for this exact reason.

When the 2 free credits run out (~7200 epochs of data per credit on metered routes), upgrade in either of two ways without re-onboarding:

- **Wallet-funded plan, in the agent**: paste the [wallet-funded one-shot](./08-openclaw-one-shot.md) — runs `signup-pay.mjs` and refreshes the API key.
- **Top-up the existing key**: `node scripts/credits-topup.mjs` with `POWERLOOM_PLAN_ID`, `POWERLOOM_EVM_CHAIN_ID`, `POWERLOOM_TOKEN_SYMBOL`, and a funded wallet — adds credits to the same `sk_live_...`.

---

## Verification provenance (cron script + one-shot)

**In `scripts/whale-cron.mjs` (already implemented):** each `bds_mpp_snapshot_allTrades` result carries `data.verification` (`cid`, `epochId`, `projectId`). The script reads that object once per poll and appends a **"Verified on-chain"** block (CID, epoch, project) to each formatted alert in `formatAlert` — it is not optional glue you add in the OpenClaw message; the one-shot above assumes this behavior. Free-key alerts carry the same verification block as wallet-funded alerts.

**Independent check:** the MCP tool `verify_data_provenance` can confirm commitments using the same `cid` / `epoch_id` / `project_id` — see [`references/03-verification.md`](./03-verification.md) and the **Verify** row in `SKILL.md` (data table).

---

## Related files in this skill

| Item | Location |
|------|----------|
| Cron entrypoint (incl. verification in alerts) | `scripts/whale-cron.mjs` |
| Pre-flight credit check | `scripts/ensure-credits.mjs` |
| Pay-signup (wallet-funded variant) | `scripts/signup-pay.mjs` |
| Top-up (more credits, existing key) | `scripts/credits-topup.mjs` |
| MCP + trade helpers | `lib/mcp.mjs`, `lib/trade-utils.mjs`, `lib/state.mjs` |
| On-chain verification details | `references/03-verification.md` |
| Wallet-funded one-shot variant | `references/08-openclaw-one-shot.md` |
| Integrator rules | `SKILL.md` → **Hosts & integrators** |

See also [`references/01-quickstart.md`](./01-quickstart.md) and [`references/06-troubleshooting.md`](./06-troubleshooting.md).
