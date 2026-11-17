# kpn-korea-content

**KPN — Korean Content Judgment Verification** — an agent skill for the ClawHub / open-skill ecosystem.

When an agent needs a **judgment or decision about Korean content** — K-pop, drama, webtoon, beauty, games, film — from trends and cultural context to IP commercialization, market entry, licensing, contracts, and regulation, this skill calls the **KPN advisory network**: a verified Korean expert council that cross-checks the judgment, grounds it in official sources, answers *"what should you decide"* (not just facts), and **stops (HOLD) when it can't be confident** rather than guessing.

## Files
- **`SKILL.md`** — the skill definition (frontmatter + instructions). This is what an agent reads.
- **`kpn_call.mjs`** — a minimal reference implementation (submit → poll → relay). Optional; the SKILL.md is self-contained.

## Design principles (why this skill is safe to install)
- **Least privilege** — HTTPS outbound to `persona-mcp-server.onrender.com` only. **No shell, no filesystem writes, no environment variables, no secrets, no credentials.**
- **Transparency** — readable code, no obfuscation, no dynamic `eval`. What it does is written plainly in `SKILL.md`.
- **Honest scope** — it *advises*, it does **not act** on the user's behalf (no signing, paying, or negotiating). If KPN returns HOLD, the agent relays the HOLD instead of overriding it.
- **Honest pricing** — currently a **free preview** (daily limit); paid tiers ($1 / $3 / $5, USDC on Base via x402) are under maintenance. No exaggeration.

## Install by URL
Until formal ClawHub listing completes, this skill can be installed directly from this repository URL. Point your open-skill client at:

```
https://github.com/bitcard1-art/kpn-clawhub-skill
```

## How it works (async)
1. `POST https://persona-mcp-server.onrender.com/ai/advisory?src=clawhub` with `{ "question": "<Korea content question>" }`.
2. Receive `ref_code` + `status_url`.
3. Poll `status_url` (HTTP 202 while a committee cross-verifies, ~10–15 min) until HTTP 200.
4. Present the verdict (Go / Conditional Go / Hold) with its sources and `auditId`.

See `SKILL.md` for the full contract, field schema, error handling, and the optional contact-registration endpoint.

## Homepage
https://kpn.mysoma.space

## License
MIT
