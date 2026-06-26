---
name: jd-triage
description: "Evaluates a job description (JD) against the user's stored career criteria and outputs a verdict with multi-axis 5-star scoring. Use when (1) the user pastes a JD with title and responsibilities, (2) the user explicitly invokes /jd-triage or asks 'should I apply for this role / 这个岗位值得投吗', (3) the user asks to update or reset their stored career criteria. On first run, bootstraps a criteria profile via structured questions; on later runs, performs a 15-day freshness check and reuses the stored profile."
---

# jd-triage

Evaluate a JD against the user's stored career criteria. Two responsibilities:

1. **Bootstrap & maintain** a personal criteria profile at `~/.openclaw/workspace/jd_criteria.md`.
2. **Evaluate** any JD the user provides against that profile, returning a verdict + 5-star scoring.

## Language

Detect the user's language from their input and respond in that language (Chinese or English supported). If the user's language is ambiguous, default to English.

| Surface | Language |
|---|---|
| Bootstrap Q&A, evaluation output, `/history` list, `/compare` table | User language |
| `jd_criteria.md` field keys, `jd_history.md` structural labels (`Evaluated`, `Verdict`, `Scores`, `Summary`, `Triggered red lines`, `Action taken`, etc.) | **Always English** (machine-readable, grep-friendly) |
| `jd_criteria.md` values, `jd_history.md` free-text content (company name, JD title, summary one-liner, red-line citations, action notes) | User language at write time — never auto-translated later |
| Verdict tier labels (`Strong Apply` / `Apply` / `Caution` / `Skip` / `OUT`) | English in stored files; translated only in UI output |

When listing or comparing history entries authored in different languages, render the structural labels in the **current user's** language but show the stored free-text content **as-is** (no translation). Auto-translation is forbidden — it loses nuance and risks introducing errors.

## State machine

On every invocation, read `~/.openclaw/workspace/jd_criteria.md` and branch:

| State | Condition | Action |
|---|---|---|
| **S1: Missing** | File does not exist | Run **Full Bootstrap**, write file |
| **S2: Schema gap** | File exists but missing fields from current schema | Ask only the missing fields, patch file |
| **S3: Fresh** | File complete and `last_updated` ≤ 15 days ago | Skip straight to **Evaluation** (mention "Using criteria from <date>") |
| **S4: Stale** | File complete and `last_updated` > 15 days ago | Ask one question: "Anything changed in salary / city / red lines / preferences? (y/n)" — `n` → refresh timestamp; `y` → user names which fields, patch only those, refresh |
| **S5: Explicit update** | User says "update criteria" / "重新填" / `/jd-triage update` / `/jd-triage reset` | Full bootstrap with current values pre-filled; user changes only what they want |

After bootstrap/refresh, if the trigger included a JD, proceed to **Evaluation**. If the trigger was an update-only request, stop after writing.

## Bootstrap

If `~/.openclaw/workspace/` does not exist, create it (`mkdir -p`). Never overwrite an existing `jd_criteria.md` without going through S5.

Ask the questions in `references/bootstrap-questions.md`. Group them into three blocks (Profile / Hard Gates / Soft Axes) and ask one block at a time, not one field at a time. After all answers are collected, show a full summary in the user's language and ask for confirmation before writing.

Write the file using the template at `assets/criteria-template.yaml`. Field keys must be English; values follow the user's language.

## Evaluation

### 1. Parse the JD

Extract: title, company name (if visible), responsibilities, requirements, comp info, location, work intensity signals (overtime / on-call / crunch language), reporting line and team structure (if mentioned).

If the JD has only a title and no responsibilities, **stop and ask the user to paste the full JD**. Do not guess.

### 2. Hard gates

Check in order. Most failures → **❌ OUT** + stop. Red-line keyword matches use the **responsibility-weight** rule below and may produce **⚠️ CONDITIONAL** instead of OUT.

- `salary_floor` — JD's stated comp must meet or exceed. If JD has no comp info, mark "unknown" and continue (do not auto-fail).
- `target_cities` — JD location must be in the list (or remote-eligible if user accepts remote).
- `lifestyle_tier` — JD's intensity signals must not exceed user's tier. Scan JD for keywords matching higher-tier patterns (see `references/scoring-rubric.md`).
- `hard_red_lines` — substring/keyword match against JD text, then apply **responsibility weight**:

  | Where the red-line keyword appears | Verdict |
  |---|---|
  | In JD title, OR in first 1–2 responsibility bullets, OR estimated to occupy >30% of role | **❌ OUT** (core responsibility) |
  | Only in tail bullets, framed as "支持/协助/辅助/support/assist", AND main responsibilities clearly fit user | **⚠️ CONDITIONAL** — proceed to soft scoring, flag the red-line bullet, and add an open question for the user to confirm with HR |
  | Appears only in "qualifications/优先" section, not in core duties | Note in open questions, do not gate |

  Cite the matched substring AND its location (which bullet, what wording) in the verdict — never just the keyword.

### 3. Soft axes (5-star scoring)

Score each axis 1–5 according to `references/scoring-rubric.md`. Never default to 3★ to fill space — if the JD lacks information for an axis, output `★★★☆☆ (info insufficient)` explicitly.

Axes:
- **Title fit** — match against `target_title_keywords`
- **Industry/track fit** — match against `target_industries`
- **Company type fit** — look up `company_type_preferences`
- **Company size fit** — look up `company_size_preferences`
- **Vibe fit** — semantic comparison of JD/company against `vibe_anchors_positive` and `vibe_anchors_negative`
- **Salary match** — relative to `salary_floor` and `current_salary`

### 4. Verdict

Map total + axis distribution to one of four tiers:

| Tier | Criterion |
|---|---|
| ✅ **Strong Apply** | All axes ≥ 4★, no axis below 3★, no hard-gate near-miss |
| 🎯 **Apply** | Average ≥ 3.5★, no axis below 2★ |
| ⚠️ **Conditional** | Red-line keyword hit in non-core responsibility (responsibility-weight rule), OR critical unknowns (salary/city/scope) that could flip the verdict — list open questions to ask HR before deciding |
| ⚠️ **Caution** | Average ≥ 2.5★ or has one critical low (e.g. vibe = 1★) — investigate before applying |
| ❌ **Skip** | Average < 2.5★ or any axis = 1★ on a high-weight dimension |
| ❌ **OUT** | Hard gate failed (core-responsibility red line, salary below floor, city mismatch, lifestyle exceeds tier) |

A single 1★ on **vibe fit** alone is enough to drop to ⚠️ Caution even if other axes are high. Vibe is load-bearing.

### 5. Log to history

After producing the verdict (regardless of outcome), append an entry to `~/.openclaw/workspace/jd_history.md`. Generate ID `JD-YYYYMMDD-XXX` (sequential per-day). Detail level follows the user's `history_detail` setting in the criteria file (default `standard`). See `references/history-format.md` for entry format.

When `history_detail = full`, prompt the user once for confirmation before storing the raw JD text (it may contain recruiter contact info / private comp).

### 6. Output template

```
Verdict: <emoji + tier>

Title fit         ★★★★☆
Industry/track    ★★★★★
Company type      ★★★☆☆
Company size      ★★★★☆
Vibe              ★★☆☆☆  ← cite anchor: "<positive or negative anchor name>", "<JD phrase that triggered>"
Salary match      ★★★★☆

One-liner: <core judgment, 1 sentence>
Action: <Apply / Confirm with HR first / Negotiate first / Backup / Skip>

Open questions (ask HR before deciding):
- <e.g. 总包范围>
- <e.g. "支持商业化"占比，是核心 KPI 还是边缘协作>
- <only include if there are real unknowns; omit section otherwise>

💡 If this evaluation changed your view on any criteria, say "update criteria".
```

For **⚠️ CONDITIONAL** (red-line in non-core responsibility), use the standard template above, but the One-liner must explicitly state the conditional clause: "Fits if <X confirmed>; OUT if <X turns out to be core>."

For **❌ OUT** (hard gate failed), use this longer form — even when skipping, surface what fit so future similar JDs are easier to spot:

```
Verdict: ❌ OUT
Triggered: <red line / failed gate, with location and exact phrase>
One-liner: <why>

Strengths matched (for future reference):
- <e.g. 新加坡/英语环境 — 命中外企偏好+海外背景>
- <e.g. Agent + RAG + Prompt 工程 — 命中目标岗位关键词>
- <only list axes with strong positive signal; omit if none>

Action: Skip
```

## History & comparison

The skill maintains a single append-only log at `~/.openclaw/workspace/jd_history.md`. Each evaluation appends one entry with a unique `JD-YYYYMMDD-XXX` ID, the verdict, scores, and the `criteria_version` used at evaluation time.

### Triggers

| Input | Action |
|---|---|
| `/jd-triage history` or "show my JD history" / "看下之前评估过的 JD" | List last 10 entries as a one-line table |
| `/jd-triage compare <id1> [<id2>]` or "compare with last one" / "和上次对比" | Side-by-side scores table |
| User refers to past JD by company name | Resolve to ID via grep on `jd_history.md`, then act |

### Criteria version

The criteria file carries an integer `criteria_version`. Increment it on every S1 / S2 / S5 write. Do **not** increment on S4 "no change" confirmations (only `last_updated` updates).

When comparing two entries with different `criteria_version` values, prepend a `⚠️ Criteria has changed between these evaluations` warning to the output.

See `references/history-format.md` for entry format, ID generation, and command details.

## Behavioral constraints

- **Don't sugarcoat.** OUT means OUT. Don't soften because the user is "already considering" the role.
- **Don't fabricate scores.** If the JD lacks info for an axis, mark "info insufficient" — never pad with 3★.
- **Don't pre-fill from training data.** Bootstrap fields come only from the user. Do not infer salary norms, city tiers, or company reputations.
- **Vibe must cite anchors.** Every vibe rating names a specific positive or negative anchor from the user's profile AND quotes the JD phrase that triggered it. Adjective-only judgments are forbidden.
- **Red lines are weighted, not literal.** Apply the responsibility-weight rule before declaring OUT. A keyword in a tail support bullet is a CONDITIONAL, not an OUT.
- **OUT still outputs strengths.** When skipping, surface what aligned (company type, language env, partial responsibility match) so the user accumulates signal.
- **Open questions are first-class.** When salary/city/scope is unknown OR a CONDITIONAL applies, output an `Open questions` list — concrete things to ask HR — instead of swallowing the unknown silently.
- **No hollow encouragement.** Skip "hope this helps" / "good luck with your search" closings.
- **Trust the criteria file.** If the user hand-edits `jd_criteria.md`, parse what's there. If a field's format is broken, point at the line and ask — don't overwrite.
- **One JD at a time.** If the user pastes multiple JDs, evaluate them one by one, not in a merged report.

## Detection triggers

Activate this skill when the user input contains any of:

- A pasted block ≥ 200 chars resembling a JD (title-like first line + bulleted responsibilities/requirements)
- Explicit invocation: `/jd-triage`, `/jd-triage update`, `/jd-triage reset`, `/jd-triage history`, `/jd-triage compare ...`
- Phrases like "should I apply", "evaluate this role", "这个岗位值得投吗", "帮我看下这个 JD", "重新填 criteria", "update my criteria", "compare with last one", "和上次对比", "看下评估过的 JD"

## Files in this skill

- `SKILL.md` — this file (main behavior)
- `_meta.json` — ClawdHub publishing metadata
- `assets/criteria-template.yaml` — template for `~/.openclaw/workspace/jd_criteria.md`
- `references/bootstrap-questions.md` — full bootstrap question set (load on first run / S5)
- `references/scoring-rubric.md` — per-axis 5-star definitions (load during evaluation)
- `references/history-format.md` — jd_history.md entry format + comparison commands (load when logging or comparing)

Load reference files only when the corresponding flow runs, to keep the main context light.
