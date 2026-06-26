---
name: iran-war-brief
description: Track the latest Iran war situation with concise 5-8 headline summaries, prioritize breaking and major events, include source links, and append a three-column verification table (US claims vs Iran claims vs third-party verifiable facts). Use when user asks for Iran conflict updates, battle damage/battle results tracking, claim verification, or rapid situation briefs.
---

# Iran War Brief

Produce a fast, verification-oriented update for Iran conflict requests.

## Output Contract

Always include, in this order:

1. **简要头条（5-8条）**
   - Keep each bullet to 1-2 lines.
   - Prioritize breaking and high-impact events (strikes, casualties, infrastructure damage, maritime chokepoints, escalation signals, official statements with concrete numbers).
   - Include publication/source time if available.

2. **新闻链接（按头条对应）**
   - One link per headline.
   - Prefer primary sources (Reuters/AP/AFP/official statements) over aggregation.

3. **三栏对照清单**
   - Table columns must be exactly:
     - 美方宣称
     - 伊方宣称
     - 第三方可核
   - Keep rows issue-based (e.g., Kharg strike, Hormuz traffic, vessel losses, air defense losses, civilian damage).
   - In “第三方可核”, clearly mark confidence:
     - 高：multi-source + evidence (satellite/photo/video/official docs)
     - 中：multi-source consistent but limited hard evidence
     - 低：single-side claim or conflicting accounts

## Sourcing Rules

Use this source priority:
1. Reuters / AP / AFP
2. BBC / Al Jazeera / major international desks
3. Regional media (Israel/Iran/Gulf) for local details
4. Official military/foreign ministry statements
5. OSINT evidence (satellite/geolocation) when available

If top-tier wire sources are temporarily unavailable, state that explicitly and proceed with best available cross-verified sources.

## Verification Discipline

- Separate **event happened** from **battle damage scale**.
- Treat words like “obliterated/destroyed totally” as claims unless independently verified.
- Prefer quantifiable fields:
  - destroyed units (count/type)
  - confirmed casualties (KIA/WIA/civilian split)
  - infrastructure status (operational/degraded/offline)
  - shipping throughput / chokepoint status
- Flag uncertainty instead of guessing.

## Response Template

Use this exact structure:

### 伊朗局势最新摘要（5-8条）
- [头条1]
- [头条2]
- [头条3]
- ...

### 新闻链接
- 1) [媒体名 - 标题](URL)
- 2) [媒体名 - 标题](URL)
- 3) [媒体名 - 标题](URL)
- ...

### 对照清单（美方宣称 vs 伊方宣称 vs 第三方可核）
| 美方宣称 | 伊方宣称 | 第三方可核 |
|---|---|---|
| ... | ... | ... |

## Style

- Write in Chinese unless user asks otherwise.
- Keep summary concise and decision-useful.
- Do not inflate certainty.