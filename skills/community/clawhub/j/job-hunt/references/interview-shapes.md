# Interview shapes, bands, and the closed tag sets

Read this **every time** you enter interview mode, before the first question — `modes/interview.md` §0 and the SKILL.md self-check both name it. It holds three things you cannot write `mock/assessment-<n>.md` without: the loop shapes, the four bands, and the two closed tag sets.

It **extends** two existing files and duplicates neither:
- `references/role-families.md` is a *CV-layout* document (what to lead with, what counts as evidence). Interviews need a different axis — what artifact the candidate must produce live. That axis is the role-family table below; the layout recipes stay where they are.
- `references/interview-prep.md` produces the thin defence brief (`interview-brief.md`) from data the pipeline already holds. This mode consumes that brief and writes back into it; it does not replace it.

## How to read the source labels

| Label | Meaning | What it may be used for |
|---|---|---|
| `[F]` | A primary page that was fetched and read | Shape **and** specific questions |
| `[C]` | A command run in-session, output quoted | Shape **and** specific questions, subject to the scraped-material rules in `modes/interview.md` |
| `[S]` | A search-result summary only; the page was never opened | **Shape only.** `[S]` material may set round count, order, and ritual names. It may never be quoted to the candidate as a specific technical question |
| `[U]` | Could not source | Do not state it at all |

Every row in the two shape tables begins with its label. A row without one is a claim with no provenance, and the doc test fails the build on it.

## Market shapes

### China (tech / campus)

| Source | Shape fact |
|---|---|
| `[F]` | The pipeline is 简历初筛 → 笔试 → 技术一面 → 技术二面 → 技术三面 → HR面 → offer, with elimination possible at every stage |
| `[F]` | 笔试 is a coding assessment before any interview; most require ACM-style input/output |
| `[F]` | 技术一面 is four parts in one round: 基础知识 + 项目 + 开放性问题 + 手撕算法 |
| `[F]` | 技术二面 goes into project depth and architecture; 技术三面 is often leadership-level, covering research direction and career plans |
| `[F]` | Rounds run 30–45 minutes. Formats: 一对一, 一对多 (common at state enterprises and banks), 多对一 / 群面 |
| `[S]` | 交叉面 exists at large firms: same-level interviewers from a different business department, no fixed round count, used to give the main interviewer an outside read |

Register notes. **八股文 is a register, not a topic** — rapid rote recall of canonical fundamentals, where the pressure is volume and speed. Running it as three thoughtful discussion questions misses the round entirely. **手撕代码 cannot be simulated here** — there is no shared editor and no watching interviewer; say so and run the verbal half instead (state the approach before coding, the complexity, what breaks on empty input).

### United States (tech)

| Source | Shape fact |
|---|---|
| `[F]` | Amazon publishes: Application → Initial screening → Interview loop → Post-interview and follow-up; the loop is "four to six intensive interviews lasting 45-60 minutes each" |
| `[F]` | Amazon's Bar Raiser is "an objective interviewer from outside the hiring team who ensures Amazon's high hiring standards are maintained" |
| `[F]` | Amazon's published pronoun guidance: use "I" statements — "Instead of saying 'we improved customer satisfaction,' say 'I implemented a new feedback system…'" |
| `[F]` | Google documents "with illustrative examples what a poor, borderline, solid, and outstanding answer would cover", and interviewers "take detailed notes of applicant responses" |
| `[S]` | The generic sequence (recruiter screen → technical phone → onsite loop → sometimes a take-home) is repeated everywhere but no primary source states it canonically |

### United Kingdom and EU public / academic sector

| Source | Shape fact |
|---|---|
| `[F]` | UK Civil Service Success Profiles has five elements: Behaviours, Strengths, Ability, Experience, Technical |
| `[F]` | Nine named behaviours, defined across seven grade groupings; the published document gives **positive examples only** ("Examples of [behaviour] at [grade] are when you:") |
| `[F]` | The published scale runs 1 Not Demonstrated → 7 Outstanding Demonstration, and every descriptor is a statement about the evidence, not about the person |
| `[F]` | Published pass bar: "A minimum score of 4 is required across all behaviours. However, candidates may score a single 3 where all other behaviour scores are high." |
| `[F]` | STAR, UK National Careers Service: Result = "what happened as a result of your action **and what you learned from the experience**" |
| `[F]` | Academic (MIT CAPD): screening interview 20–40 min; campus visit 1–2 days; job talk 45 min–1 hour; a chalk talk on future research plans; sometimes a teaching demo |
| `[S]` | UK academic panels score against the person specification as "the only basis for scoring", marks per criterion fixed at the outset, panel of three or more reaching consensus |
| `[S]` | EPSO uses eight general competencies composed of observable "anchors"; the list itself is only in PDFs that could not be decoded |

The academic loop's **meal and hallway are scored informally**. A module that rehearses only the job-talk Q&A misses the failure mode that actually sinks candidates.

### Netherlands

| Source | Shape fact |
|---|---|
| `[F]` | Multiple interviews are normal: hiring manager, then the team, then possibly leadership |
| `[F]` | Directness is the house style — anything questionable on the CV will be asked about without preamble; vague answers are penalised, data and concrete results expected |
| `[F]` | Non-hierarchical workplaces: teamwork evidence is load-bearing |
| `[F]` | The local method is **STARR** — Situatie, Taak, Actie, Resultaat, **Reflectie** (what did you learn, what would you do differently, what feedback did you get); **STARRT** adds Transfer, how you will apply it |
| `[S]` | A case *opdracht* may precede the first or second interview; psychometric assessment scales with seniority; the process closes with an *arbeidsvoorwaardengesprek* held after the decision and before signature |

The reflectie step **is a scored element, not politeness.** A perfect STAR that stops at Resultaat is an incomplete Dutch answer. That is the single cheapest high-value correction this mode makes for an NL target, and a US-calibrated mock never surfaces it.

### Germany

| Source | Shape fact |
|---|---|
| `[F]` | Five phases: greeting/small talk, application questions and self-presentation, company presentation, candidate questions, farewell |
| `[F]` | 45–60 minutes (Robert Half: 30–60), with "kein Jobinterview gleicht dem anderen" |
| `[F]` | The interviewer may come from Geschäftsführung, Personalabteilung, or Fachabteilung depending on company size |
| `[F]` | Legally impermissible questions are listed (family planning, sexual orientation, health, religion, political beliefs, union membership, finances) and the candidate "muss nicht ausweichen oder sich rechtfertigen" |
| `[U]` | Whether German private-sector hiring normally runs multiple rounds. Two fetched sources describe a single five-phase interview and neither states a round count. **Do not assert a German multi-round loop.** |

For DE/AT/CH targets the prohibited-question list is a rehearsal item **in the opposite direction**: what the candidate needs is a prepared polite refusal, not a prepared answer.

## Role-family shapes

Keyed on what the candidate must produce live. This is the interview axis; `references/role-families.md` keeps the CV axis.

| Source | Live artifact demanded | Families | Can this mode run it? |
|---|---|---|---|
| `[F]` | Working code, watched | SWE, ML eng, quant | **Partly** — the verbal half only. No shared editor exists; say so rather than faking it |
| `[S]` | A design argued aloud | SWE system design, ML system design, data experiment design | **Yes** — text-native, the strongest mode here |
| `[F]` | A prepared talk | research scientist, academic, senior clinical, some PM | **Yes, via file** — the candidate outlines, you play the Q&A |
| `[S]` | A defended past artifact | research scientist, PhD track, legal, creative | **Yes** — deep-dive on a real paper, repo, or matter the candidate names |
| `[S]` | A live role-play with a counterpart | sales, clinical comms, teaching, hospitality, consulting | **Yes** — you play the counterpart |
| `[F]` | Structured evidence against named criteria | UK/EU public sector, NHS, academic, EU institutions | **Yes** — and the criteria are published, so the rubric is not invented |
| `[F]` | Rote recall at speed | China tech 八股文, some licensing exams | **Yes** — but as volume, not as three questions |
| `[S]` | Values scenarios, deliberately non-clinical | NHS and other regulated professions (MMI) | **Yes** — and the classic failure is answering with clinical knowledge |

For a family not listed, ask one question that resolves the whole shape: **"In your field, what does the employer make you do live — talk, demonstrate, be scored against written criteria, or be role-played at?"** The answer picks a row above and everything else follows.

## The four bands

Bands are **not numbered**, so they cannot be averaged into a score that has no referent. They are worded as evidence-presence, in the style of the one published scale that does this honestly: every COPFS descriptor is a statement about what appeared in the room, not about the person.

| Band | Descriptor |
|---|---|
| `not_present` | Nothing in the answer addresses this. Quote the closest thing the candidate did say |
| `asserted` | The candidate stated it but gave no occasion, no object, and no detail that could be checked ("I'm good at stakeholder management") |
| `instanced` | A specific, dated-or-datable occasion with named people, systems, or numbers, volunteered unprompted |
| `held_under_probe` | Instanced, **and** the candidate supplied a further concrete detail when asked for one they had not already given |

**`held_under_probe` is the ceiling, and that is deliberate.** The published Civil Service scale has a 6 and a 7 for "exceeds expectations at this level" — awarding those requires knowing what that level expects, and this mode does not know. What was observed is that an answer survived one real dig. That is what the top band says.

`contradicted` is **not a fifth band.** It is an orthogonal flag: the answer conflicts with the CV, with `interview-brief.md`, or with an earlier answer this session. It is never scored — it is emitted as `tag=CONTRADICTED` by the provenance pass and it escalates to the walk-back list.

Bands are emitted per question against five dimensions: `instance`, `completeness`, `ownership`, `outcome`, `probe`. There is no `provenance` dimension — provenance is decided by pass 2, which is the only pass holding the provenance map.

## Defect tags (closed set)

Emitted **with the verbatim line that triggered them**. No quote, no tag — `check_mock.py` fails on a tag whose `quote=` is empty or does not appear in the transcript.

| Tag | Fires when | Emitted by |
|---|---|---|
| `PROBE-COLLAPSE` | Under follow-up the candidate withdrew, hedged away from, or contradicted their own original claim | pass 1 |
| `UNSOURCED-FACT` | A figure, tool, employer, title, or scope appears in the answer that is in neither the profile, nor `interview-brief.md`, nor an earlier answer this session | pass 2 |
| `OVER-CLAIM` | The stated scope or credit exceeds the source fact recorded in `interview-brief.md` | pass 2 |
| `CONTRADICTED` | The answer conflicts with the CV, with `interview-brief.md`, or with an earlier answer this session. Quote both sides | pass 2 |

`PROBE-COLLAPSE`, `OVER-CLAIM`, and `CONTRADICTED` make a `## Walk-back list` section mandatory. `UNSOURCED-FACT` does not: its usual honest resolution is "true, just not on my CV", which is a `claims.yaml` entry, not a CV edit.

## Answer-shape tags (closed set)

Facts about the shape of the answer. Same rule: no quote, no tag.

| Tag | Fires when |
|---|---|
| `NO-INSTANCE` | A general practice, not a specific time ("I always make sure to…") |
| `NO-OUTCOME` | The answer ends without saying what changed |
| `VAGUE-OUTCOME` | An outcome word with no object ("it went really well", "it was a success") |
| `NO-ACTOR` | "We" throughout; the candidate's own action is not separable |
| `PREAMBLE-HEAVY` | More than half the answer elapses before the first action the candidate took |
| `DRIFT` | The answer finishes on a different question than the one asked |
| `NO-REFLECTION` | **NL targets only** — no reflectie step, which STARR treats as a required element |
| `NO-TRADEOFF` | A design or decision answer presents one option and no alternative considered |
| `JARGON-UNGLOSSED` | A domain term used undefined to an interviewer the candidate was told is non-expert |
| `NO-NEXT-STEP` | **Sales role-play only** — the call ended without asking for a next step |
| `CLINICAL-DRIFT` | **Regulated/values interview only** — a values scenario answered with clinical knowledge |

## Verbatim question material

Only `[F]` and `[C]` material may be quoted to the candidate as a specific question. This section holds what has been read directly and may be used as-is:

- `[F]` The Civil Service scale wording, quoted and attributed, as a checklist of what the panel is told to look for — never as a prediction of the mark.
- `[F]` The STAR / STARR element definitions, including the Dutch reflectie and transfer steps.
- `[F]` Amazon's published "I" vs "we" instruction, used to explain what the Ownership dimension is looking for.
- `[C]` Any question opened with `opencli nowcoder detail <id>`, subject to every rule in `modes/interview.md` (date stamp shown, country rule, 12-month rule, answers never pasted).

Everything else in this file is shape. Search-summary material sets round count, order, and ritual names, and stops there.
