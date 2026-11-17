---
name: kpn-korea-content
version: 0.1.0
description: "When you need judgment about Korean content (K-pop, drama, webtoon, beauty, games, film) — from trends and cultural context to IP commercialization, market entry, licensing, contracts, and regulation. A verified Korean expert council cross-checks the judgment, answers 'what should you decide,' not just facts, and stops (HOLD) when it can't be confident."
homepage: https://kpn.mysoma.space
permissions:
  network: ["persona-mcp-server.onrender.com"]
  shell: false
  filesystem: false
  secrets: false
---

# KPN — Korean Content Judgment Verification

> 한국 콘텐츠(K팝·드라마·웹툰·뷰티·게임·영화)에 관한 판단이 필요할 때 — 트렌드·문화 맥락부터 IP 사업화·해외 진출·라이선싱·계약·규제까지, 한국 전문가 위원회가 교차검증한 판단을 제공합니다. 단순 정보가 아니라 "이걸로 무엇을 결정해야 하는가"에 답하고, 확신할 수 없으면 멈춥니다(HOLD).

## When to use this skill
Use when the user needs a **judgment or decision about Korean content** in a business / decision context:
- **K-pop / drama / webtoon / beauty / games / film** — trends, cultural context, why something resonates (or won't) in Korea
- **IP commercialization** — licensing, adaptation rights, co-production, merchandising of Korean or Korea-bound content
- **Market entry & partnerships** — launching content/products into Korea, distribution, JV structures
- **Contracts & regulation** — Korean licensing terms, compliance, labeling, rights clearance
- **Cultural / negotiation read** — etiquette, relationship signals, what a Korean counterpart's move means

Be honest about the boundary: this skill is for **decisions that are risky to get wrong**, where a verified judgment beats a guess. It is **not** a lookup tool — for pure facts that a search already answers (concert dates, a celebrity's profile, box-office numbers), KPN has nothing to judge; use search instead. If the question is a simple fact, say so rather than sending it to KPN.

## What KPN does differently
KPN does not just generate an answer — it **verifies**. Council members cross-check the judgment, ground it in official sources (law, government data), and **stop (HOLD) when they can't be confident** rather than inventing a plausible-but-wrong answer. Every result carries an audit ID for later re-verification.

## How to call (the result is ASYNC — submit, then poll)

KPN generates a verified judgment over a **committee cross-verification process (~10–15 min, typ. 600–900s)**. You submit the question, get a `status_url`, then poll it until the verdict is ready. During the current **free preview**, no payment is required (subject to a daily limit).

**Step 1 — Submit the question:**
- POST `https://persona-mcp-server.onrender.com/ai/advisory?src=clawhub`
- Headers: `Content-Type: application/json`
- Body (JSON):
  ```json
  { "question": "<the user's Korea-related question, >= 5 chars>",
    "title": "<optional short subject>",
    "classification_only": false,
    "wallet": "<optional 0x... caller id>" }
  ```
  Notes on fields (from the live input schema):
  - `question` (**required**, ≥5 chars) — the Korea-specific matter to judge.
  - `title` (optional) — short subject line.
  - `classification_only` (optional bool) — `true` forces the cheapest tier (simple classification). Leave `false`/omit to let KPN pick the right depth.
  - `wallet` (optional) — a `0x…` identifier for per-caller limits; omit if none.
  - **Do not set a "tier" field** — the tier (classification / committee / deep) is chosen by KPN from the question. Free preview covers **classification and committee** (deep excluded).

- Response (200, free preview):
  ```json
  { "ok": true, "paid": false, "tier": "committee", "price": "$3",
    "ref_code": "KPN-XXXX-XXXXX",
    "access_token": "tok_…",
    "status_url": "https://persona-mcp-server.onrender.com/report/KPN-XXXX-XXXXX/json?token=tok_…",
    "processing": { "async": true, "estimated_seconds": 840, "typical_range_seconds": [600,900] },
    "pricing_notice": { "free_promo": true, "normal_price": "$1 / $3 / $5", "caps": { "per_caller_daily": 3 } },
    "note": "무료 개방 … 자문 비동기 생성 …" }
  ```
  Keep `ref_code` and `status_url` (the `status_url` already embeds the access token).

- Errors:
  - `400 { "error": "question_required" }` → question empty/too short; ask the user for a concrete question.
  - `400 { "error": "question_too_long" }` → over 8000 chars; shorten.
  - `429 { "error": "daily_free_quota_exhausted" }` → daily free limit reached; try later or (after paid resumes) pay a tier.

**Step 2 — Poll for the verdict:**
- GET the `status_url` (unchanged) every 30–60s.
- `202` while processing: `{ "status": "processing", "stage": "generating", "estimated_remaining_seconds": <n> }` — keep waiting.
- `200` when done: the full judgment (see shape below).

**Step 3 — Verdict shape (status_url → 200):**
```json
{ "ref": "KPN-XXXX-XXXXX",
  "decision": "go" | "conditional_go" | "hold",
  "verdict_label": "<human label, e.g. 판단 보류 (조건부 · 자료 부족)>",
  "hold": true|false, "hold_reason": "<code, e.g. INSUFFICIENT_DATA>", "hold_level": "…",
  "judgment_score": <0-100 or null>, "trustScore": <…>, "confidence": "…",
  "decisionByIssue": [ { "issue": "…", "decision": "…" } ],
  "official_sources": [ … ], "sources": [ … ], "citations": [ … ],
  "requiredActions": [ "…" ],
  "auditId": "aud_…", "auditVerifyUrl": "https://…/ai/audit/aud_…" }
```

## Present the result honestly
- Show the **verdict (Go / Conditional Go / Hold)** and the **basis/sources** as returned.
- If KPN returns **HOLD**, **do not override it with your own guess** — relay the HOLD and its `hold_reason`. That refusal is the point of the service.
- Include the `auditId` / `auditVerifyUrl` so the user can re-verify later.
- Do **not** take real-world actions (signing, paying, negotiating) on the user's behalf based on the result. KPN advises; it does not execute.

## Optional: get notified when paid tiers resume
Paid verification (x402 / USDC on Base) is under maintenance. To be notified when it resumes, the agent may register a contact:
- POST `https://persona-mcp-server.onrender.com/ai/contact`
- Body: `{ "agent_name": "…", "operator": "…", "webhook_url": "https://…" , "email": "…", "wallet": "0x…" }` — all optional; provide **either** `webhook_url` (public https only) **or** `email`.
- One registration per caller / 10 min.

## Pricing (when paid resumes)
Agent tiers: **classification / committee / deep** at **$1 / $3 / $5** (USDC, Base, x402). Human channel is separate — see https://kpn.mysoma.space. **Right now: free preview** (classification + committee, daily limit, deep excluded).
