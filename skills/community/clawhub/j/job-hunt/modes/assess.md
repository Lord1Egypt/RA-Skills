# Mode: assess — decide whether to apply

**Entry condition:** a posting exists — a URL, pasted text, or a row the user named from
a shortlist. Nothing else in this file runs until step 1 has produced usable text.

**This mode owns** `posting.yaml`, `posting-source.txt`, `cv-source.txt`,
`evidence-blocks.json`, `fit-assessment.yaml`, `fit-assessment.md`, `coverage.json`.
It reads `profile.yaml` and never writes it except through a confirmed online-presence write-back. Resolve the workspace with
`paths.workspace(name, company, role, today_iso)` using today's local ISO date — never by joining strings. That
one function owns the shape `~/.claude/job-profiles/<name>/applications/<company>-<role>-<YYYY-MM-DD>/`,
which is byte-identical to the old skill's so "resume an unfinished application" keeps
working; a run that builds its own path breaks resumption silently.

---

## Supplementary public research

Use `references/supplementary-sources.md` when official web/news, WeChat
public accounts or relevant GitHub projects can fill a concrete career evidence
gap. It defines source selection, availability checks and evidence quality.
These sources supplement formal posting evidence; select only what the current
question needs.

## 0. Enter the mode — as soon as the workspace can exist

The workspace name needs the company and role, and those come from the posting. So
read the posting text first (§1 decides whether you actually have it), take the
company and role from it, create `paths.workspace(...)`, and run this before writing
any artifact into it:

```
python3 scripts/paths.py --name "<meta.name>" --company "<company>" --role "<role>"   # prints <ws>, absolute
python3 scripts/enter_mode.py --workspace <ws> --mode assess \
    --because "<why assess, in one line, from what the user asked>"
```

`check_assessment.py` refuses to pass without this record (`NO_MODE_ENTRY`) or when this
file changed afterwards (`MODE_FILE_CHANGED`). Read this file in full after running it.

## 1. Fetch-integrity gate — a 200 OK is not evidence you have the posting

LinkedIn, Workday, Greenhouse, Lever, Taleo, iCIMS and most portals return a success
status for a login wall, a cookie banner, a bot check or a search page. Extracting
must-haves off a login wall produces a document that is internally consistent and
entirely wrong, and every later step inherits it.

| Reading | Verdict |
|---|---|
| The specific role and employer are identifiable, with substantive duties and requirements and no indication that the description is truncated | **usable** — proceed, even for a concise posting or a language without spaces |
| A login / consent / bot-check wall replaces the description, or the result is a search card, empty shell or visibly truncated excerpt | **blocked** — recover the full text with the available reader or ask the user to paste it |
| Completeness remains ambiguous | explain what appears missing and ask; never invent requirements |

Word count is a warning signal, not a minimum. A complete short Chinese posting
can be usable; a long login page cannot. An incidental sign-in link does not make
an otherwise complete description inaccessible. Already-pasted complete text
needs no fetch merely to satisfy a tool step.

Save whatever you got, verbatim and unedited, as `posting-source.txt`. That file is the
end of the source chain for every downstream claim — editing it makes provenance
theatre. If the posting genuinely cannot be obtained, follow the refusal floor in
§8 before stopping: save the refusal record and explain the missing input. Do not
skip that record merely because this is Step 1. Never proceed on guessed requirements.

## 2. Market — ask, do not infer

Ask the user which market this role is in. Do not match place names: a wrong market card
reads exactly like a right one and the reader has no source text to check it against.
If `search-preferences.yaml` already holds a target market, confirm it **once per
session** rather than once per posting — but re-ask whenever the posting's location does
not match the stored market. That file is written by discover mode; if it does not
exist, just ask. Never write it from here.

Markets with tables: `cn`, `nl`, `de`, `uk`, `us`. Anything else → set
`market: other` in `fit-assessment.yaml`, explain in the user's language that no
convention data is available for that market, and render no
convention card at all. The sixth token is `other`, never `none` — one spelling, so two
gates cannot disagree about the same word. **Never substitute a neighbouring market's
conventions.**

## 3. Extract `posting.yaml` — the complete field list

Twelve names, in this order — matching the canonical extraction table in
`references/job-posting-extraction.md` and the declaration in `modes/apply.md`
Step 2. The entry skill routes here instead of repeating the schema.
The source repository's test suite checks these declarations so a mode cannot
omit a field that a downstream gate requires.

```yaml
role_title: "..."          # exactly as written in the posting
company: "..."             # the exact public employer name
seniority: mid             # intern | junior | mid | senior | lead
location: "..."            # the posting's own location text, verbatim, one string
must_haves: []             # required / essential / minimum / "you must"
nice_to_haves: []          # preferred / bonus / a plus / ideally / advantageous
responsibilities: []       # what the person will actually do, in the posting's words
keywords: []               # exact ATS terms, casing preserved: "PyTorch", "CI/CD"
company_values_tone: "..."
red_flags: []
salary_range: null         # the stated band, or null
application_type: cv       # cv | structured
```

Three fields carry weight far past their size:
- `company` — the **exact public employer name**. `apply` mode names the workspace
  directory from it and `check_letter.py` verifies the letter's recipient against it,
  emitting `NO_COMPANY_IN_POSTING` — a hard finding — when this field is absent. Every
  apply run downstream of an assess run that skipped it fails on that line.
- `salary_range` — when present, ask the user **once** whether the band fits. A band
  mismatch is a common silent screen-out and is cheaper to surface now than after a
  full application. If no range is stated, keep it unknown. Mention that absence
  when it affects the user's decision or stated pay floor; never invent a band
  or require a salary answer before assessing the available evidence.
- `application_type` — `structured` when the employer requests a supporting
  statement, criterion-by-criterion evidence, a competency response or a structured
  application form. Essential / Desirable headings alone are not enough.
  It is the **only** signal that routes to a
  supporting-statement deliverable in `apply`. Getting it wrong produces a perfectly
  good CV for a process that does not read CVs.

There is no `language` field here: the CV language lives in the profile's `meta.language`.

Non-English cue words map the same way: `Erforderlich` / `Voraussetzungen` /
`Sie bringen mit` → must_have; `Wünschenswert` / `von Vorteil` → nice_to_have;
`Exigé` / `Requis` → must_have; `Souhaité` → nice_to_have; `必须` / `必备` → must_have;
`歓迎` / `尚可` / `加分` → nice_to_have.

## 4. Disqualifiers first, and ask

A disqualifier is a wall, not a wish: work authorization, a legally required licence or
clearance, a hard on-site requirement, language fluency, a regulated experience floor.
Surface these **before anything else** and ask the user directly whether they meet them.
No reframing closes a legal barrier, and a "mitigation" that treats one as a wording
problem reads to a recruiter as already handled.

**The mechanical form, because "surface it first" is not checkable and this rule is too
important to leave uncheckable.** Whenever any requirement row is `screening: knockout`
with `match: gap` or `match: no_evidence`, `fit-assessment.md` opens with a
`## 硬性阻断项` section, **above** the counts block, and that section names every such
row **by its id**:

```markdown
## 硬性阻断项

- **R2** — 该岗位要求你已经持有欧盟工作许可。这是法律层面的门槛，不是表述问题。
- **R5** — 岗位要求本地注册执业资格。
```

Writing in English? The heading is `## Hard blockers`. For Japanese, Korean or
Spanish, read [report-localization.md](../references/report-localization.md) and use
the matching native heading. The exact heading identifies this required section.

Native report anchors (the full templates and placement rules are in the language
contract). Use one language throughout; the gate accepts these exact labels:

| Element | ja | ko | es |
|---|---|---|---|
| Blockers heading | `## 応募を妨げる必須条件` | `## 지원을 막는 필수 조건` | `## Requisitos excluyentes` |
| Next-action heading | `## 次に取る方針` | `## 다음 행동` | `## Qué hacer a continuación` |
| Acceptance column | `確認基準` | `완료 기준` | `Criterio de aceptación` |
| Deliverable column | `成果物` | `산출물` | `Entregable` |
| Verdict marker, emitted by count_coverage | `応募の判断：` | `지원 판단:` | `recomendación de candidatura:` |
| Required disclaimer anchor | `結果を予測するものではありません` | `결과를 예측하는 것이 아닙니다` | `no es una predicción del resultado` |
| Stale-review banner | `再確認期限を過ぎています` | `재검토 기한이 지났습니다` | `ha vencido la fecha de revisión` |

**Write the answer down, in the two §6 fields built for it.** What the posting demands
goes in `stated_conditions` (a `type`, a `stance`, and an evidence ref to the JD block
it came from); what the user told you goes in `declared_work_status` — their own words
about their own status, never inferred, and `unknown` when the answer was not clear.
`consistency.py` compares the two and prints `NOTICE_WORK_AUTH_CONFLICT` or
`NOTICE_WORK_AUTH_VERIFY`, which always say *these two appear to conflict, check it
yourself* and never *you are not eligible*. Asking and then not recording the answer
leaves those notices unable to fire at all (`WARN_NO_WORK_STATUS`), and a misspelled
token switches them off silently (`BAD_WORK_STATUS`, `BAD_STATED_CONDITION`). This is a
second line behind the knockout row below, not a replacement for it.

Write the barrier in your own words, in the reader's language. The **id** is what
`check_assessment.py` keys on: `NO_DISQUALIFIER_SECTION` (section absent),
`DISQUALIFIER_NOT_NAMED` (a blocking row's id missing), `DISQUALIFIER_AFTER_VERDICT`
(section below the verdict line).

## 5. Cut evidence blocks

Run the online-presence step first (`references/online-presence.md`,
`scripts/online_presence.py status --name "<name>" --workspace <ws>`), so confirmed
public work is in the master before `cv-source.txt` is taken from it.

```
python3 scripts/evidence_blocks.py --workspace <ws> \
    --jd <ws>/posting-source.txt --cv <ws>/cv-source.txt
```
`cv-source.txt` is the CV text this assessment cites — paste, or a copy of the master
profile. Do not hand-write `evidence-blocks.json`; it is derived.

**What blocks buy, stated honestly and carried into your output:** a reference that
resolves guarantees the claim points at something real. It does **not** guarantee the
claim follows from it. It is a plausibility bound, not a proof.

## 6. `fit-assessment.yaml` — the complete schema

This schema is defined here and nowhere else; `check_assessment.py` and three other
scripts read both halves.

**The top level. `level_direction` and `effort` are PRINTED on the coverage card in §7.**

```yaml
market: cn                      # vocab.MARKET_KEYS (cn | nl | de | uk | us), or
                                # vocab.NO_MARKET ("other") when no table applies.
                                # Never "none" — the sixth token is "other" everywhere.
verdict: worth_applying         # one of the five, or insufficient_evidence
provisional: false              # always false in an assessment; discover rows carry true
effort: evening                 # overall: quick | evening | multi_day | not_closable
level_direction: lateral        # step_up | lateral | step_down | unclear
declared_work_status: needs_sponsorship
                                # authorized | needs_sponsorship | student_or_graduate
                                # | temporary_route | unknown
stated_conditions:              # work-authorization style conditions read off the posting
  - type: sponsorship           # sponsorship | work_authorization | citizenship | clearance
                                # | licence | onsite_location | other
    stance: requires_existing   # requires_existing | offers_support | unclear
    evidence: [{ref: JD-004}]
actions:                        # the single authoritative to-do list
  - action: "Publish the torchrun port"
    acceptance: "Repo README shows a two-GPU run log"
    when: before_apply          # now | before_apply | later
conventions_rendered: [cn-boss-profile-is-the-screen]
```

Top-level `effort` prices closing the gaps **as a whole**; a row's `effort` prices that
row. Set the top-level one by reading your rows. `consistency.py` prints
`NOTICE_VERDICT_EFFORT` for `strong_apply` beside `multi_day` or `not_closable`.

**`level_direction` and `effort` are required** because the card prints them:
`check_assessment.py` fails with `MISSING_LEVEL_DIRECTION` / `MISSING_EFFORT` when either
is absent or out of enum, on every verdict except the §8 refusal. A missing one renders
as 「未评估」 / `not assessed`, which is never a value you may write.

`declared_work_status` is the user's **own statement**, from the §4 question — never
inferred from a name, a university, or a location. `unknown` is a real answer and the
right one when you did not get a clear reply; it suppresses both work-authorization
notices, which is the safe direction, so `check_assessment.py` only warns
(`WARN_NO_WORK_STATUS`) when the field is missing. What it does **not** tolerate is a
value outside the set: `consistency.py` compares a `stance` against this field and
returns nothing for any token it does not recognise, so a hyphen in `needs-sponsorship`
switches the notice off and leaves a card that looks clean. That is `BAD_WORK_STATUS`,
and `BAD_STATED_CONDITION` for the same fault in a `type` or a `stance`.

**The requirement rows.** One row per must-have and per named responsibility.

```yaml
requirements:
  - id: R1
    kind: must_have          # must_have | responsibility
    text: "the requirement in the posting's own words"
    level: required          # required | preferred | unclear   — what the posting CALLS it
    screening: knockout      # knockout | weighted | nice_to_have — what it DOES at screening
    match: partial           # strong | partial | gap | no_evidence
    recency: recent          # current | recent | dated | undated
    effort: evening          # quick | evening | multi_day | not_closable — to close THIS row
    how_to_close: "..."      # "" when nothing closes it
    evidence: [{ref: CV-012}]
```

`level` and `screening` are separate axes on purpose, and it is the least obvious win
here: most "required" lists are wish-lists, and counting the label is exactly what turns
a missing clearance from a **stop** into a score deduction.

Row rules, enforced by `check_assessment.py`:
- `match: no_evidence` → `evidence: []`. Every other row needs at least one ref that
  resolves. An absent citation never means the thing is absent — it means nobody cited it.
- Print every row in `fit-assessment.md` **with its evidence reference**. That is what
  makes the denominator auditable and lets a reader object to one line rather than to
  the whole number. Block ids belong in that table and nowhere else in the prose.

## 7. Countable facts, no score

Run `python3 scripts/count_coverage.py --workspace <ws> --lang <user language>` (zh|en|ja|ko|es;
the default is zh, while `consistency.py` defaults to en, so always pass it) and paste its block verbatim
into `fit-assessment.md` inside a fence. It is the **only** counting path; a second
number written by hand will fail the gate.

```
必备条件有充分证据：   8 项，共 11 项   （部分符合 2，存在缺口 1，无证据 0）
核心职责已证实：     4 项，共 6 项
职级匹配：           平级
可补缺口所需投入：   一晚
投递建议：           大概率被筛掉
```

The block follows the **user's** language, not the market's. `count_coverage.py`
supports `--lang zh|en|ja|ko|es`; the [language contract](../references/report-localization.md)
provides the corresponding required report text. The English block uses English
labels:

```
must-haves strongly evidenced:   8 of 11   (partial 2, gap 1, no evidence 0)
core responsibilities demonstrated: 4 of 6
level match:                     lateral
effort to close the gaps:        evening
apply verdict:                   likely_screen_out
```

The verdict marker is load-bearing: `check_assessment.py` recognises the five
language-specific labels produced by `count_coverage.py`. Paste its output unchanged;
do not translate the label or recompute the numbers by hand.

The strongly evidenced count takes `strong` only. `partial` and `gap` are never merged into a covered
number. Evidence that is only `dated` counts as `partial`.

The two count lines are computed from the §6 rows; 「职级匹配」 and 「可补缺口所需投入」 are
read straight off the top-level `level_direction` and `effort`.

**Required disclaimer, immediately under the block. Use the matching language's
template unchanged; Japanese, Korean and Spanish are in the
[language contract](../references/report-localization.md):**

> ⚠️ 以上是对证据的清点，不是对结果的预判。每一项都连同它的证据引用一起印出，分母可以逐条审计；
> 本 skill 不给出面试或录用的可能性估计，也不给 0–100 分。要不要投，由你决定。

> ⚠️ This is a count of evidence, not a forecast of the outcome. Every item is printed
> with its evidence reference so the denominator can be audited row by row. This skill
> states no interview or hiring outcome estimate and no 0–100 score. Whether to apply
> is your call.

The disclaimer is what stops a count being read as a prediction. `check_assessment.py`
looks for 「不是对结果的预判」, "not a forecast of the outcome", or the corresponding
Japanese, Korean or Spanish anchor in the language contract.

## 8. The refusal floor — insufficient evidence, no verdict

Set `verdict: insufficient_evidence` and print **no** coverage block and **no** verdict
from the five-level list when any of these holds:
- the posting could not be read,
- the CV could not be read,
- an image source has regions you cannot make out,
- the CV is a skills list with no supporting entries behind it.

Even an early fetch failure must leave `fit-assessment.yaml` with
`verdict: insufficient_evidence`, empty `requirements`, `stated_conditions`,
`actions` and `conventions_rendered` lists, plus `fit-assessment.md` explaining
the unreadable input and the concrete next input needed. Preserve any captured
source. Do not invent employer, market, evidence blocks or missing requirements
to complete the normal assessment schema; do not claim the full assessment gates
passed when their inputs are absent.

Say what you could not read and what you need. **When the input cannot support a
conclusion, a confident positive conclusion is forbidden.** This is a floor, not a sixth
verdict level: it is orthogonal to the ordered five, because "I could not read the
input" is not a point on that scale.

## 9. Market convention cards — verbatim, id-allowlisted

Print the table's run-time half instead of opening the YAML:

```
python3 scripts/convention_cards.py --market <market> --lang <user language>
```

For every entry in `references/market-conventions/<market>.yaml` it prints, copied
verbatim from the table, exactly what this step uses: the `id`, `applies_when`,
`review_by` and the reader text (`text_zh` for zh, `text_en` for en, both for ja/ko/es;
`--text zh|en` overrides; `--table <file>` reads a table the session names instead of the
shipped one). The `source`, `why` and `unverified` fields are the
maintainer's review trail and never reach a card, so do not read the YAML itself. Render
only entries whose `applies_when` is satisfied, and render `text_en` / `text_zh`
**character for character**. You may not author, strengthen or extend an entry, attach a
number to one, or invent one.

**If an entry's `review_by` has passed, still render it, with a 「已过复核期」 banner.**
`convention_cards.py` flags such an entry on its `review_by` line, with the banner in
your `--lang`, using the same date check the gate uses.
A date going by while the code did not change should not stop the skill working. The CI
lint (`check_conventions.py --ci`) fails on the expired date so a person fixes it; the
runtime gate downgrades it to `WARN_EXPIRED_REVIEW_BY` and instead requires the banner
string 「已过复核期」 to appear in `fit-assessment.md` (`MISSING_STALE_BANNER`). On an
English card the banner is **"past its review date"** — like every other anchor in this
file it is a pair, and the card follows the user's language. Rendering a stale card
without telling the reader it is stale is the one thing that is worse than either.

The one sentence you write in this section is where **this CV** stands against the
convention, and it cites CV blocks like any other claim. List the ids you rendered in
`conventions_rendered:`.

Conventions feed **neither the verdict nor any consistency check**. They are the one
class of claim with no source text behind them; keeping them out of the arithmetic is
what stops an unciteable assertion moving a citeable conclusion.

## 10. When the verdict is likely_screen_out or blocked: the other half

A verdict without this half is a door closed with nothing behind it. Produce all three,
under a `## 那该怎么办` heading — `## What to do instead` if you are writing in English.
For Japanese, Korean or Spanish, use the heading and table labels from the
[language contract](../references/report-localization.md). Strategy tokens stay unchanged.

**(a) Exactly one strategy**, from this closed set — not two, not a menu:

| Strategy | Use it when |
|---|---|
| `apply_anyway` 投了再说 | The gap is soft and the cost of applying is an evening |
| `reposition` 重新定位 | The same evidence reads much better against a different role family |
| `skill_sprint` 技能冲刺 | One named, closable requirement is doing all the blocking |
| `side_door` 侧门切入 | A contract, internal transfer, adjacent team or smaller employer reaches the same work |
| `change_track` 换方向 | The blocking requirement is structural and not worth closing for this goal |

Write the chosen token literally — `check_assessment.py` counts how many of the five
appear **inside that section** and fails on zero (`NO_STRATEGY_SECTION`) and on more
than one (`STRATEGY_NOT_UNIQUE`). A menu is not a recommendation; picking is the work.
Naming a rejected strategy in the same section counts as a second one, so contrast it
in prose above the heading, or name it without its token.

**(b) A 30/60/90 table** with exactly these columns:

| 目标 | 行动 | 验收标准 |
|---|---|---|
| ... | ... | ... |

In English: `| Goal | Action | Acceptance criterion |`.

**(c) A roadmap carrying an 输出物 (`Deliverable`) column.**

`验收标准` and `输出物` — or `Acceptance criterion` and `Deliverable` — are where the
entire value of this section sits. They are what turn advice into something checkable,
and `NO_ACCEPTANCE_COLUMN` fails the gate when neither spelling of either column header
is present. Every row of both tables must also appear in
`actions:` in `fit-assessment.yaml`; that list is the single authoritative to-do list,
and `consistency.py` compares it against the closable gaps.

## 11. Gates — run all of them, in this order

```
python3 scripts/evidence_blocks.py     --workspace <ws>   # step 5, listed again for order
python3 scripts/count_coverage.py      --workspace <ws> --lang <user language>
python3 scripts/consistency.py         --workspace <ws> --lang <user language>
python3 scripts/check_evidence_refs.py --workspace <ws>
python3 scripts/lint_no_prediction.py  --workspace <ws>
python3 scripts/check_assessment.py    --workspace <ws>
```

`check_assessment.py` runs last on purpose: it reads the other five gates' receipts out
of `journal.jsonl` and refuses to pass if any of them is missing (`MISSING_RECEIPT`) or
recorded a failure (`UPSTREAM_FAILED`). Re-deriving their answers instead would let a
gate that was never run look identical to a gate that passed.

Attach every notice `consistency.py` printed beside the thing it qualifies. Notices
**report and never repair**: code can see two fields disagree, it cannot see which one
is right, and choosing silently would swap a visible contradiction for an invisible
guess.

**Never report success without a receipt.** A skipped gate produces no output, and that
looks exactly like a clean one. `check_assessment.py` writes the receipt that lets you
say this passed.

## Write the client report from the checked findings

Keep `fit-assessment.*` internal: its complete evidence rows, exact counts and
required disclaimer still pass the existing gates. Write `report.md` separately
for the job seeker using `references/report-writing.md`. Lead with the decision,
explain relevant experience and real gaps, and order the next actions. Do not copy
the internal record, raw coverage block, repeated IDs or engineering disclaimer.
A zero count of fully demonstrated responsibilities must not erase useful partial
experience from the explanation. Preserve the assessment's facts and uncertainty.

## Hand the artifacts over

Follow SKILL.md "Client deliverables": write `report.md` (read
`references/report-writing.md` first), render and review it, run
`lint_no_prediction.py`, then `python3 scripts/deliver.py --workspace <ws>` last (client files go to `~/Downloads/<workspace-name>/`). A
source CV is not redelivered unless the user asks (`--include-applications`). Do not
start another mode automatically.

## 12. Self-check before you hand this over

- [ ] `scripts/enter_mode.py --mode assess` ran before anything else, and this file was
      read in full after it.
- [ ] `posting-source.txt` is verbatim and unedited; `posting.yaml` carries all twelve
      fields, including `company`, `salary_range` and `application_type`.
- [ ] Disqualifiers were asked about, and a `## 硬性阻断项` section names each blocking
      row **by id**, **before** the verdict.
- [ ] Every requirement row prints its evidence reference; no block id appears in prose.
- [ ] `fit-assessment.yaml` carries the top-level fields too, not just the rows:
      `level_direction` and `effort` are both set and both in enum — the card prints
      them, and 「未评估」 on a shipped card means nobody judged a line the reader will
      read as judged.
- [ ] The §4 work-authorization answer is recorded: `declared_work_status` (`unknown`
      is a legal answer) and a `stated_conditions` entry for what the posting demands.
- [ ] The coverage block is the one `count_coverage.py` produced, byte for byte.
- [ ] The disclaimer is present, unchanged, directly under the block.
- [ ] No percentage, no `n/m` score, no prediction word — except a quoted employer
      rubric with its source named on the next line.
- [ ] Convention cards are verbatim from `references/market-conventions/<market>.yaml`
      as `scripts/convention_cards.py` printed them, `applies_when` was honoured, and
      `conventions_rendered` lists their ids.
- [ ] Any rendered entry whose `review_by` has passed carries the 「已过复核期」 /
      "past its review date" banner, in the card's own language.
- [ ] Every consistency notice that fired is attached where it fired.
- [ ] If the verdict is 大概率被筛掉 or 硬性阻断: **exactly one** strategy token from the
      closed set, a 30/60/90 table with a `验收标准` column, and a roadmap with an
      `输出物` column — all mirrored into `actions:`.
- [ ] A discover-stage 「基于卡片信息的初判」 verdict was **not** copied in. assess
      always recomputes.
- [ ] `check_assessment.py` exited 0 and its receipt is in `journal.jsonl`.

**Voice.** Follow `references/report-writing.md` for the client report: address the job seeker directly, lead with the decision, explain the real strengths and gaps, and give concrete next actions. Keep row-level evidence references and coverage disclosures in `fit-assessment.*`.
