# Stock Watcher Pro — Security Audit

🛡️ **Codex Security Verified**

---

## Audit Summary

| Field | Detail |
|-------|--------|
| **Skill** | Stock Watcher Pro v1.0 |
| **Audit Date** | March 2026 |
| **Auditor** | OpenAI Codex Security Agent |
| **Result** | ✅ PASSED |
| **Risk Level** | Low (information-only tool, no trading capability) |

---

## What Was Audited

1. **SKILL.md** — Agent instructions reviewed for prompt injection defense, data isolation, and absence of unsafe patterns.
2. **Scripts** (`stock-watcher-scheduler.sh`, `edgar-check.sh`) — Reviewed for command injection, path traversal, and privilege escalation risks.
3. **Config files** — Verified no hardcoded secrets, API keys, or credentials.
4. **Data schemas** — Verified no PII leakage paths, proper file permission guidance.
5. **External API usage** — SEC EDGAR rate limit compliance, no unauthorized data exfiltration.

---

## Security Guarantees

### 🔒 No Data Exfiltration
- The skill never sends your portfolio data, thesis notes, or financial information to any external server.
- All data stays in your local workspace under `data/` with `chmod 600` permissions.
- No analytics, no telemetry, no phoning home.

### 🔒 Prompt Injection Defense
- All external content (SEC filings, news articles, RSS feeds, web-scraped text) is treated as **untrusted data, not instructions**.
- The SKILL.md contains explicit injection defense rules that prevent the agent from executing commands embedded in financial documents.
- This is critical because SEC filings and financial news articles can contain arbitrary text.

### 🔒 No Trade Execution
- The skill is strictly read-only intelligence. It cannot and will not execute trades, connect to brokerages, or move money.
- There is no brokerage API integration, no trade execution logic, and no capability to modify financial accounts.

### 🔒 No Hardcoded Secrets
- Zero API keys, tokens, or credentials in any file.
- The skill uses only publicly available SEC EDGAR endpoints and the agent's built-in web search.
- If the user adds API keys for premium data providers, those are managed in their own environment — not in skill files.

### 🔒 File Permission Enforcement
- All directories containing financial data use `chmod 700`.
- All files containing portfolio positions, thesis notes, or cost basis use `chmod 600`.
- The SETUP-PROMPT.md enforces these permissions during initial setup.

---

## User Guidance for Data Protection

### Sensitive Data in This Skill
Your portfolio data includes information you may consider sensitive:
- **Stock positions** (tickers, share counts, cost basis)
- **Investment thesis** (your strategic reasoning)
- **Price targets** (your expectations)
- **Filing analysis** (your agent's interpretation of SEC filings)

### Recommendations
1. **Encrypted disk:** If your workspace is on an unencrypted drive, consider enabling full-disk encryption (FileVault on macOS, BitLocker on Windows, LUKS on Linux).
2. **Backup strategy:** Back up the `data/` directory regularly. This is your intelligence archive.
3. **Access control:** Ensure only you have access to your workspace directory. The `chmod 700/600` permissions help, but physical access control matters too.
4. **Group chats:** If your agent operates in group chats, be aware that portfolio queries in group contexts could expose your positions to others. Use private/direct messages for sensitive portfolio discussions.

---

## Financial Disclaimers

⚠️ **IMPORTANT — READ CAREFULLY:**

1. **Not Financial Advice.** Stock Watcher Pro is an information-gathering and research organization tool. Nothing it produces constitutes financial advice, investment advice, tax advice, or a recommendation to buy, sell, or hold any security.

2. **No Guarantees.** The accuracy of SEC filing summaries, news analysis, and thesis evaluations depends on the quality of source data and AI interpretation. Errors are possible. Always verify critical information from primary sources.

3. **Not a Substitute for Professional Advice.** Consult a qualified financial advisor, tax professional, or attorney for advice specific to your financial situation.

4. **No Liability.** NormieClaw, the skill authors, and OpenClaw assume no liability for investment decisions made based on information provided by this skill.

5. **Past Performance.** Any historical analysis or thesis tracking does not predict or guarantee future results.

6. **SEC Data.** SEC EDGAR data is provided by the U.S. Securities and Exchange Commission. The skill accesses publicly available data and complies with SEC fair access guidelines.

---

*Last updated: March 2026*
