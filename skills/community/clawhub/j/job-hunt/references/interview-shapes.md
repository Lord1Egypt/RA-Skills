# Interview shapes, bands, and the closed tag sets

Read this **every time** you enter interview or prepare mode, before the first question — `modes/interview.md` §0 and the SKILL.md self-check both name it. It holds three things you cannot write `mock/assessment-<n>.md` without: the loop shapes, the four bands, and the two closed tag sets.

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

Register notes. **八股文 is a register, not a topic** — rapid rote recall of canonical fundamentals, where the pressure is volume and speed. Running it as three thoughtful discussion questions misses the round entirely. **手撕代码 can be run here, except for the watching.** A `coding` round has the candidate state the approach and its complexity first, then write the code, which is run against hidden cases (`references/preparation.md` §3). What cannot be simulated is an interviewer watching them type under time pressure. Say so rather than pretend.

### China (public sector: 公务员)

| Source | Shape fact |
|---|---|
| `[F]` | 国考（中央机关及其直属机构）公共科目笔试：上午行政职业能力测验（9:00—11:00），下午申论（14:00—17:00）；面试由招录机关实施；综合成绩一般笔试、面试成绩各占一半，组织专业能力测试的职位另行合成（新华网，2025-11-30） |
| `[S]` | 面试以结构化面试为主，部分职位采用无领导小组讨论（一组约 5–7 人）；行测题型包括常识判断、言语理解与表达、数量关系、判断推理、资料分析 |

A 公务员 candidate's preparation is mostly **the written exam**, not the interview: two papers set nationally, then a structured interview the 招录机关 runs. A plan that starts with the interview has the order backwards.

### United States (tech)

| Source | Shape fact |
|---|---|
| `[F]` | Amazon publishes: Application → Initial screening → Interview loop → Post-interview and follow-up; the loop is "four to six intensive interviews lasting 45-60 minutes each" |
| `[F]` | Amazon's Bar Raiser is "an objective interviewer from outside the hiring team who ensures Amazon's high hiring standards are maintained" |
| `[F]` | Amazon's published pronoun guidance: use "I" statements — "Instead of saying 'we improved customer satisfaction,' say 'I implemented a new feedback system…'" |
| `[F]` | Google documents "with illustrative examples what a poor, borderline, solid, and outstanding answer would cover", and interviewers "take detailed notes of applicant responses" |
| `[S]` | The generic sequence (recruiter screen → technical phone → onsite loop → sometimes a take-home) is repeated everywhere but no primary source states it canonically |

### United States (federal and general)

| Source | Shape fact |
|---|---|
| `[F]` | OPM (federal hiring): in a structured interview "all candidates are asked the same predetermined questions in the same order", scored on one rating scale; it asks about "behavior in past experiences and in proposed hypothetical situations", usually with a panel reaching consensus |
| `[S]` | Behavioural questions ("Tell me about a time when…") are standard in US university career guidance; a case interview gives a business problem and scores the reasoning; McKinsey pairs each case with a Personal Experience Interview |

### United Kingdom (all sectors)

| Source | Shape fact |
|---|---|
| `[F]` | nidirect (UK government): an interview "can be as quick as 20 minutes or might involve assessment over a number of days", in one format or a mixture |
| `[F]` | Telephone or video interviews are a common first stage, used to screen many candidates quickly; a call may come "out of the blue" |
| `[F]` | Panel interviews: "Normally two or three people" ask questions in turn |
| `[F]` | Assessment centres are used by "Employers from every industry", "most common for graduate schemes, retail employers and businesses like call centres"; they may involve written tests, group activities and interviews |
| `[F]` | Psychometric tests are used "either at the application or interview stage" |
| `[S]` | Civil Service: online tests (verbal, numerical, judgement, work strengths), and assessment combining an interview, a presentation, a written exercise and/or a role-play; strengths questions sit beside behaviour questions |
| `[S]` | NHS: values-based recruitment is national guidance; trusts tie questions to their values (one trust names the 6Cs); nursing selection may add multiple mini-interviews or an assessment day |
| `[S]` | Teacher training: the process varies by provider; candidates are advised to prepare safeguarding scenarios; teaching a lesson or activity is common but not universal |

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
| `[F]` | Randstad NL: an assessment is part of "sommige sollicitatieprocedures", used "vooral bij functies met veel verantwoordelijkheid"; usually intelligentietests, persoonlijkheidsvragen, an interview and praktijkcases (rollenspel, postbakoefening), half a day to a full day; the candidate reads the psychologist's report first and decides whether the employer receives it |
| `[F]` | IGJ, a Dutch government inspectorate: eerste gesprek (motivation, experience, skills), tweede gesprek (job content, team, fit), an assessment for leadership and senior functions after the second gesprek, then the arbeidsvoorwaardengesprek |

The reflectie step **is a scored element, not politeness.** A perfect STAR that stops at Resultaat is an incomplete Dutch answer. That is the single cheapest high-value correction this mode makes for an NL target, and a US-calibrated mock never surfaces it.

### Germany

| Source | Shape fact |
|---|---|
| `[F]` | Five phases: greeting/small talk, application questions and self-presentation, company presentation, candidate questions, farewell |
| `[F]` | 45–60 minutes (Robert Half: 30–60), with "kein Jobinterview gleicht dem anderen" |
| `[F]` | The interviewer may come from Geschäftsführung, Personalabteilung, or Fachabteilung depending on company size |
| `[F]` | Legally impermissible questions are listed (family planning, sexual orientation, health, religion, political beliefs, union membership, finances) and the candidate "muss nicht ausweichen oder sich rechtfertigen" |
| `[F]` | Bundesagentur für Arbeit: Assessment-Center are common for duale Studiengänge, öffentlicher Dienst, Banken, Versicherungen and internationale Konzerne, and for Ausbildung at large firms and Trainee-Programme; half a day to two days |
| `[F]` | AC exercises: Selbstpräsentation (2 bis 3 Minuten), Gruppendiskussion, Postkorb-Übung (prioritise tasks or e-mails under time pressure), Rollenspiele (with a Kunde or Kollege), Leistungstests (Logik, Konzentration, Zahlenverständnis, Sprachgefühl), Einzelinterview; also Präsentationen and Fallstudien |
| `[F]` | AC observers assess Teamfähigkeit, Kommunikation, Selbstbewusstsein, Problemlösung, Zuverlässigkeit und Auftreten |
| `[F]` | Interview questions "beziehen sich meistens auf deinen Lebenslauf, deine Berufswahl, das Unternehmen und deine Persönlichkeit"; listed examples: why us, Stärken, Schwächen; the candidate should be able to present the Lebenslauf freely and keep every statement consistent with the application |
| `[U]` | Whether German private-sector hiring normally runs multiple rounds. Two fetched sources describe a single five-phase interview and neither states a round count. **Do not assert a German multi-round loop.** |

For DE/AT/CH targets the prohibited-question list is a rehearsal item **in the opposite direction**: what the candidate needs is a prepared polite refusal, not a prepared answer.

## Role-family shapes

Keyed on what the candidate must produce live. This is the interview axis; `references/role-families.md` keeps the CV axis.

| Source | Live artifact demanded | Families | Can this mode run it? |
|---|---|---|---|
| `[F]` | Working code, watched | SWE, ML eng, quant | **Mostly**, as a `coding` round: the candidate's code runs against hidden cases. Being watched while typing cannot be simulated. Say so rather than faking it |
| `[S]` | A design argued aloud | SWE system design, ML system design, data experiment design | **Yes** — text-native, the strongest mode here |
| `[F]` | A prepared talk | research scientist, academic, senior clinical, some PM | **Yes, via file** — the candidate outlines, you play the Q&A |
| `[S]` | A defended past artifact | research scientist, PhD track, legal, creative | **Yes** — deep-dive on a real paper, repo, or matter the candidate names |
| `[S]` | A live role-play with a counterpart | sales, clinical comms, teaching, hospitality, consulting | **Yes** — you play the counterpart |
| `[F]` | Structured evidence against named criteria | UK/EU public sector, NHS, academic, EU institutions | **Yes** — and the criteria are published, so the rubric is not invented |
| `[F]` | Rote recall at speed | China tech 八股文, some licensing exams | **Yes**, as a `knowledge` round, but as volume, not as three questions |
| `[S]` | Values scenarios, deliberately non-clinical | NHS and other regulated professions (MMI) | **Yes** — and the classic failure is answering with clinical knowledge |
| `[S]` | A business case reasoned aloud | consulting, strategy, some finance and product roles | **Yes** — text-native; give the case data piece by piece as it is asked for |
| `[F]` | Timed ability tests (numerical, verbal, logical; 行测) | graduate schemes, public sector, banks and insurers (the UK, DE, NL and China rows above) | **Partly**, as a `knowledge` drill of original practice items. The real test's timing, norms and difficulty cannot be reproduced; say so |
| `[F]` | Assessment-centre exercises (in-tray / Postkorb / postbak, self-presentation, group discussion) | graduate and trainee schemes, public sector (the UK, DE and NL rows above) | **Partly**: in-tray prioritisation, a self-presentation and a role-play run here; a live group discussion cannot, because there are no other candidates |

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
