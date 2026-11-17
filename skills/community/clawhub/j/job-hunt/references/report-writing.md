# Write a report the client can use

Read this before drafting or revising client-facing career reports in any mode.
It applies to `report.md`, explanations in shortlists and assessments, interview
advice, and the final hand-off. It supplements the language contract; it does not
rewrite source quotations, schema keys, IDs, required labels or computed counts.
It covers what the report says and how it reads. Rendering, layout review and
`deliver.py` follow SKILL.md "Client deliverables" and
`references/layout-review.md`; the few delivery points they do not repeat are
under "Delivery" below. A report that compares several postings (discover, or a
ranking of supplied postings) also reads `references/discover/multi-posting-report.md`.

Before delivery, remove internal test narration from the whole report, including
the title, body and footer. A fictional-profile test still produces a sample
client report: do not insert fixture provenance such as “固定虚构履历” or describe
which software test stages ran. Store that provenance in the private test record.
Telling a real client what this practice round covered (“本轮只练了技术面”) or
that a mock is not a real interview is ordinary advice, not test narration.
Turn any useful result into concrete preparation advice without inventing actual
user interview performance. The delivery marker check is a backstop; reading the
whole report for its intended audience remains mandatory.

## Client advice and internal evidence are separate artifacts

`fit-assessment.yaml`, `fit-assessment.md`, `coverage.json` and any before/after
`fit-snapshot.md` are internal analysis records. Keep their complete evidence rows,
stable IDs, computed counts and exact required disclaimers for the checks. Do not
copy those records into `report.md` or use them as the client PDF source. Do not
copy an internal `completion.md` into it either. Tool defects, adapter errors,
tests, developer diagnostics and internal review logs belong only in the private
workspace.

Write `report.md` independently from the checked findings, in the client's
language. Start with whether the
role is worth applying to, then explain the evidence that supports it, the gaps
that change the decision, and the next actions in order. Cite useful source facts
near the claim (for example, the specific CV experience or an original posting
link); the client does not need `JD-001` / `CV-001` in every cell. Use the same
facts and verdict as the internal record, but ordinary language and a structure
that answers this client's question. Do not print raw coverage blocks, the
denominator-audit explanation, or wording about what “this skill” can output.

For example, partial responsibility evidence calls for explaining the relevant
work and the missing ownership. A bare “0 of 4 demonstrated” can obscure real
experience; keep that mechanical count internal and say what the client has
actually done. Never convert a partial into a demonstrated result to improve the
headline. Do not invent an outcome probability, and do not write a numberless
certainty about the outcome either (肯定能拿到面试, 进面稳了, "you will definitely get
an interview"); `lint_no_prediction.py` blocks both. Saying which topics an
interview is likely to cover is preparation, not prediction. When the user explicitly asks
to see the evidence counts, explain their scope once and link the detailed record.

Full consultations normally include a PDF and editable text. Explicit chat-only,
no-file or format requests take precedence. A supplied bullet rewrite stays in
chat and does not create a report, workspace or independent review workflow.

## Readability before brevity

Remove words that do no work, not words that make the explanation understandable.
Keep the full subject, necessary connectors such as “因为 / 但 / because”, and
the consequence for the reader. If an edit makes the reader reconstruct what a
noun refers to or reread the sentence, it is too compressed. For example, “先核实
年限再补材料” is less useful than “先问招聘方是否认可你现有工作的相关经验，再决定
是否为这个岗位准备项目材料”. A detailed report should explain the reasoning fully.

Use two editing passes. First subtract warm-ups, vague praise, stock contrasts
and repetition. Then add whatever the reader needs to understand the judgment:
the relevant requirement, the actual experience, an unresolved question or a
specific next action. This second pass adds reasoning, not an invented personal
voice, an anecdote, a number or another slogan.

## Start with the reader's decision

Tell the reader what to do and why: which roles to examine first, what prevents
a decision, or what to prepare. A heading should identify its subject without
requiring the previous page: “北京优先考虑的三个岗位”, not “优先方向 1/2”;
“Check sponsorship before applying”, not “Strategic considerations”.

Separate three things in the explanation: what the posting or CV actually says,
what you infer from it, and what you suggest doing. “Your CV does not describe a
product launch” is not “You have never launched a product”. An undisclosed salary
is not evidence that a pay floor is met, even after the prose is polished.

Preserve explicit employer information without adding speculative uncertainty.
If a title says “深圳/北京” while a location badge only says “深圳”, display both
cities from the title. The shorter badge alone does not establish that Beijing
is uncertain. If useful, describe the field difference briefly in a note rather
than attaching “待确认” to the location. Reserve uncertainty labels for a real
unresolved conflict or missing information that affects the client's decision.

Explain the basis of an ordering instead of only saying “再看某类岗位”. Tie the
priority to the actual requirements, documented experience and preparation effort.
Do not infer that a client is mainly To C, or unsuitable for To B/platform work,
from personal apps or content projects alone. Distinguish using an API from owning
a platform product's requirements, release, compatibility and enterprise use cases;
describe which responsibilities are documented and which are still missing.

For a long report, use a short decision summary and a contents page with useful
section names and working page links. Put comparable jobs in a table or use
consistent field labels. Explain each count's unit and exclusions once near the
count; do not make the reader reconcile postings, grouped roles and closed jobs.
Client usefulness decides what earns space: explain limitations that affect the
next decision, without turning internal query bookkeeping into report content.

## Keep narrative categories aligned with their table

For a summary and the table it introduces, choose the grouping once. Draft the
summary from the table's final categories and rows; after changing a category,
update both. Use the **same category names, level of detail and relative order**.
A summary may discuss selected categories, but name them as the table does and
make that selection clear. Do not make the reader infer the mapping from later
job details or a separate explanation.

If both broad groups and specific directions are useful, show their relationship
in the same table (for example, separate group and direction columns), and use
those same labels in the prose. Do not list “金融软件、知识图谱、APS” in the
paragraph while showing only “软件与技术产品” in the table.

In a role-comparison table, identify the company **and specific job title** for
each role. A column called “岗位” must contain positions, not only company names.
Keep different specializations at one company on separate rows; a shared company
name cannot stand in for several jobs. Retain the grouping rules for exact
company-and-full-title matches across locations in `references/discover/multi-posting-report.md`.

For example, a summary discussing “金融软件、知识图谱、APS” in that order can
map directly to this illustrative table; actual reports use the source titles:

| 方向 | 公司 | 职位 |
|---|---|---|
| 金融软件 | 甲公司 | 金融软件产品经理 |
| 知识图谱 | 乙公司 | 知识图谱工具产品经理 |
| APS | 乙公司 | APS 工具产品经理 |

Check each summary/table pair before rendering and again in the final PDF:
trace every named direction to the same visible category and its company/title
rows. Reject missing mappings, unexplained changes of level or order, and
company-only lists that hide distinct roles. This is a semantic reader review;
text-presence and layout checks cannot certify it. A multi-posting report's
separate source directory may still group entries by company.

## Make a detailed report easy to navigate

Cite the original posting link near the claim it supports; do not append a
separate source/methodology/scope chapter that reproduces the internal source
audit. Keep ownership verification chains, annual-report
page references, collection windows and commentary about restrictions the
posting never stated in the private research notes. If a finding affects the
decision, give its practical conclusion once with the relevant job, such as an
application deadline or a specific contract question; do not narrate how the
evidence was checked. This does not remove the need to do and retain that work.

Place the table of contents after the report title and brief metadata, before
the first numbered section. Do not place it after the first section's narrative
or table. Verify that order in both the editable text and rendered PDF, and
check the actual page destinations after pagination.

Let numbered sections continue on the current page when room remains. Do not
force the second section, or every section, onto a new page merely to preserve
a previous page count. Keep headings with following content, then inspect every
page for avoidable blank areas and a lone trailing table row. Adjust ordinary
spacing or table padding while retaining the approved font sizes; never add
empty space or shrink text to meet an arbitrary number of pages.

When following a report example, copy its information structure as well as its
typography; matching only fonts and colors is insufficient. Scale the rows to the
actual evidence; never copy the example's job count or fabricate entries to fill it.

Give adjacent sections different jobs in the reader's workflow. For example,
application preparation answers what to confirm before applying, which CV/version
to use or revise, and what to check before sending. Interview preparation answers
which questions to practise, how to explain real decisions and outcomes, and what
to ask the interviewer. Put the full case preparation in the interview section;
refer to it briefly elsewhere only when that reference advances a distinct action.
A sequence of similarly titled preparation lists is not a coherent workflow.
Name the role a tailored CV or interview plan targets, especially when the report
compares several roles; distinguish an existing deliverable from a suggested
future version. These are section purposes, not mandatory headings or counts.

Review structure explicitly after rewriting. Compare the reference and output's
table columns, field labels, numbering, grouping and links in both Markdown and
PDF. A single summary table does not replace all of the example's lists, and a
rewrite must not flatten the reference's lists and tables into continuous prose. Record
this comparison in the layout review under `content_order` and
`headings_and_rules`; missing lists or tables require another formatting pass.

Keep the approved typography; follow `references/word-resume-layout.md` for the
English Times New Roman and Chinese SimSun report convention and its language,
template and user-request exceptions. Verify the embedded fonts in the output.
The default consultation palette is white paper with navy emphasis (`#17365d`),
very pale blue table alternation (`#f5f7fd`) and light blue rules (`#c5d2e3`).
A newer user palette or supplied template takes precedence. A request to borrow
colors does not authorize copying a reference's fonts, spacing or entire layout.

Use a compact conclusion, a clickable contents page for a long report and clear
section headings. Put the
job requirement, the client's relevant experience, what remains uncertain and
the next action close together. Use stable comparison labels, not unexplained
“1/2” group names. Preserve the detailed reasoning and useful interview preparation.
Use space for this information; avoid decorative blank areas, repeated warnings,
compressed fragments and smaller type merely to fit more on a page. Check page
balance, table wrapping, link labels, contents targets and all report versions.

Default to a conventional written report, not a presentation deck. Use continuous
sections and ordinary paragraphs; a new section does not automatically need a new
page. As a starting point, use 12 pt body text, 14 pt section headings, a 16–18 pt
document title, 1.35–1.5 line spacing and modest paragraph spacing. Tables may use
11–12 pt when readable. A later explicit size or supplied report template wins.
In Markdown, use one H1 for the document title, H2 for sections and H3 for roles
or subtopics, so the renderer can preserve that visual hierarchy.
Write contents entries as Markdown links to heading anchors; the bundled renderer
resolves them after pagination. Do not hard-code page numbers into the source.
The bundled renderer lays out a table of more than four columns as one labelled
paragraph block per row, not a grid, and prints `**bold**` as plain text. Keep a
comparison table to four columns when it should read as a table, and do not rely
on bold to carry meaning.
Keep figures at reading size rather than turning counts into oversized statistic
cards. Use comparison tables where they help, with no card frame around every
recommendation. A compact linked contents block can share the opening page.

Remove subtitles and lead-ins that explain the document instead of the jobs.
For example, delete “这些岗位也已读完整要求。表中说明了哪些可以继续了解，哪些暂时不值得
优先准备。” and “每个方向都给出准备材料与需要回答的问题。” Start with the actual
judgment, requirement or preparation material. Do not systematically add a gray
explanatory sentence beneath every heading. Keep dates, genuine evidence-status
labels and useful source qualifications; they carry information.

If the reader says the type looks large, measure the current body and heading
sizes before changing them. Reduce oversized headings, card padding and forced
page breaks first. A proposed larger point size will not make a report denser;
explain that briefly and use a sensible standard size when the user's number was
only an example. Preserve substantive analysis during reflow rather than cutting
it to fit. Inspect the new pages at normal reading scale.

For a revision, maintain a private acceptance list covering every explicit user
correction, not just the latest one. Check that list against every final PDF and
the shared skill instructions: prose, layout, fonts, palette, source titles,
grouped cities and links, excluded closed roles, and justified uncertainty. Rerun
relevant repository checks and actual report generation; passing text-based tests
alone cannot establish that the output meets the user's layout requirements.

## Replace abstraction with something the reader can identify

Name the person, task, document, action or result behind an abstract phrase.
“补证据” should say whether you mean a project description, prototype, test
record, release note or a clarification from the candidate. “跨团队交付” should
say who worked together, what the candidate did and what was delivered, when the
sources establish those details. If the details are unknown, ask for them or state
the gap; do not invent a realistic-sounding example as the candidate's history.

These are editing examples, **not replacement macros**. Their facts must be
supported in the actual case.

| Before | More useful wording |
|---|---|
| 现有经历与该方向相邻，具备一定迁移价值。 | 你做过批量评测，这个岗位也要求设计评测指标，值得先读它的完整要求。 |
| 补充端到端产品闭环的证据。 | 整理一个真实项目，说明需求从哪里来、你决定了什么、功能怎样上线、上线后看了哪些数据。 |
| 强化跨职能协同与结果导向意识。 | 简历还没说清你与研发怎样合作。选一个实际参与的项目，写清你的责任和验收方式。 |
| 从能力到业务，构建差异化竞争力。 | 面试时解释：这个功能解决了谁的问题，你怎样判断它值得做。 |
| 薪酬区间存在不确定性，建议进一步核验。 | 招聘页没写薪资。先问固定税前月薪是否达到你的要求，再决定是否花时间准备。 |
| Leverage transferable competencies to demonstrate end-to-end ownership. | Describe one real project: what you decided, who you worked with, what shipped, and how you checked the result. |

Use technical terms when they matter to the role; explain an unfamiliar one on
first use, in the reader's language. Keep employer names and exact job titles
unchanged in the source directory. In your explanation, introduce “PRD（产品需求
文档）” before using PRD alone. Do not replace a precise term such as API, RAG or
clinical registration with a vague synonym just to sound less technical.

## Remove formulaic prose without removing substance

- Delete introductions that merely announce the next sentence, repeated
  conclusions, and advice that could be pasted unchanged into any client's report.
- Remove meta-commentary such as “本文将 / 这里要说清楚 / let me be clear” and
  self-praise for the report's rigor. Describe the source limitation itself:
  “招聘页没有写薪资”, not “本报告坚持审慎核验薪酬信息”. Put only limitations that
  affect the client's decision in the report; keep tool diagnostics private.
- Rewrite literal translations, strings of abstract nouns, slogan-like endings,
  and repeated “不是……而是……”, “从……到……”, “既……又……更……” constructions when
  they obscure the point. A real comparison can stay; a rhetorical flourish
  should not carry the reasoning.
- Prefer connected sentences with a clear subject and action. Do not turn each
  clause into a bullet, force every paragraph into three parts, or replace one
  template with the same new sentence pattern throughout the report. Consistent
  labels in a comparison table help reading and are not a prose defect.
- Give actions a real subject. Replace “市场会奖励复合能力” with the particular
  requirement an identified employer published. Do not upgrade ordinary English
  such as “use” and “make” into “leverage” and “facilitate” for a professional tone.
- Name the actual object: the CV, the experience the client described, a job
  advert or a specific work record. Do not blur them into “现有材料” or narrate
  an internal evidence assessment when the reader needs an action. For example,
  “简历还没写出连接器延期的处理结果；面试前补清最后的到货安排” identifies both
  the missing detail and the next step. Keep a real distinction between missing
  experience and a detail merely absent from the CV; do not turn clearer prose
  into a new factual claim.
- Lead preparation advice with what to do or explain. Put a relevant honesty
  boundary beside that action once; avoid making every section another list of
  things the client must not say. This does not remove real gaps or authorize
  invented achievements, numbers or first-person interview scripts.
- Address the client directly. An anonymized public example may say “示例中的
  求职者”, but should not sound like an internal assessment of a person who is
  absent from the conversation. Do not invent anecdotes or casual slang to
  manufacture a human voice.
- Keep substantive reasons, employer requirements, real gaps, source links and
  useful preparation detail. A request for a detailed report is not an invitation
  to pad it with repeated cautions; a request for plain language is not a request
  for a shorter report.

Apply the method in the requested language, using natural local phrasing rather
than translating the Chinese examples word for word. These are editorial
judgments, not a universal blacklist or an “AI probability” score. A vocabulary
lint can suggest places to reread; it cannot certify readability, and it must not
rewrite job quotations or fail a table merely for repeating a useful label.

## Review the rendered report before delivery

This is a separate full-report review step, not a few wording checks folded
into drafting or a synonym for layout inspection. Complete it for every report:

1. Read the current report from beginning to end without relying on the private
   work notes to fill gaps. Include summaries, every table and the directory;
   reading only changed passages or excerpts is not a full read.
2. Assess **reasonableness**: recommendations follow the real job requirements,
   client constraints and known experience; gaps and proposed actions agree.
   Assess **logic**: the recommendation, selection and preparation form a clear
   sequence, identities agree and adjacent sections have distinct purposes.
   Assess **readability**: the client can understand the terms, references and
   next steps without internal assessment language, needless repetition or an
   explanation from the author. Use the detailed questions below.
3. Correct the findings, then reread the entire revised report for regressions
   and broken transitions. Repeat when a substantive issue remains. Do not
   preserve a known contradiction merely because each section reads well alone.
4. After rendering, read the final PDF from first page to last and perform the
   visual/link review. Content or order changes after that invalidate the full
   read. Record the reviewed revision (source/PDF fingerprint), concrete findings,
   corrections and remaining issues in private work notes. Stop delivery if an
   unresolved issue makes the advice unsupported, contradictory or unclear.

A brief clean-review record should state the actual recommendation/action chain
checked, not just “全文通读：PASS”. Never invent a full read, an independent
reviewer or a numerical readability score. Script receipts check their own
inputs; they do not establish these editorial judgments. Spot checks, a clean
lint and layout hashes cannot substitute for this full read.

First fix passages the user has identified. Then read the whole report as its
intended reader, checking (a multi-posting report adds the two job-identity
questions in `references/discover/multi-posting-report.md`):

1. Can I find the recommendation and its reason without reading every page?
2. Does each important judgment name the relevant job requirement and what the
   supplied background does or does not establish?
3. Can I carry out each proposed next step? Replace “加强/完善/补齐” on their own
   with the actual thing to ask, prepare or verify.
4. Is each unfamiliar term explained, each heading meaningful, and each paragraph
   adding information rather than restating another paragraph?
5. Did the revision preserve facts, uncertainty, sources, consent boundaries and
   distinctions between completed work and suggestions?
6. Do adjacent sections answer different reader questions, with a clear next
   action? Trace any repeated case across sections: each occurrence must add a
   distinct purpose rather than repeat the same preparation or warning.
7. Are the target role, CV version, existing work and suggested next steps clear?
   Replace vague “material/evidence” references with the actual object, then check
   that the rewrite preserved what is known, missing or still to be confirmed.
8. Does each summary use the same category names, level and relative order as
   its table? Trace each named direction to visible company-and-title rows;
   correct any mapping the reader would have to infer from another section.

For a long report, compare pages as well as individual sentences. Look for the
same paragraph opening, rhetorical reversal, overused bolding or repeated
conclusion across sections. Keep the stable labels needed to compare jobs;
change repetitive narrative only where it makes the report easier to read.
After changing a claim or label, search every requested version for its old
wording, including the summary, contents and closing advice. A new body with an
old summary is not a completed revision.

Read any rewritten paragraph aloud or as ordinary speech to catch awkward
translations and overloaded sentences. Record representative before/after fixes
and any unresolved issue in the private work notes; do not add a review scorecard
to the client's report or claim an independent review that did not happen.

Rerun the existing prediction/evidence checks relevant to changed claims, then
render and inspect the final pages, contents links and external links. Preserve
approved fonts, colors and layout preferences. For a reader who prefers detail,
use the available space for useful comparisons and explanations, not decorative
blank areas, repeated text or smaller type. Review all requested language and
public/private versions for shared leftover phrasing before delivering them.

## Method sources and adaptation

The editorial method is adapted from the supplied `martin-writer`, its
`long-doc-rewrite` reference, `martin-writer-en`, and the bilingual
`ai-flavor-remover` skills. `zimeiti-copywriter` contributes the use of one
reviewed master when producing multiple versions. Their source notes credit
humanizer-zh, stop-slop, ai-flavor-remover, HC3, humanizer, human-writing,
Wikipedia's Signs of AI writing and writing-agent. This reference contains the
career-report method; none of those skills or checkers is a runtime dependency.

Keep the readability-first, subtract-then-add, source-integrity and whole-document
review ideas. Do not import the originals' social-platform hooks, first-person
persona quotas, engagement requests, fixed word/frequency budgets, automatic
style scores or universal punctuation bans. Career reports retain the client's
formatting choices, necessary questions, exact quotations and source links.

## Delivery

Render, review and deliver as SKILL.md "Client deliverables" and
`references/layout-review.md` describe; they own the commands, the folder layout,
the format acceptance review and the byte-for-byte PDF rule. Points they do not
repeat:

- `deliver.py` requires `report.md` and a verified report PDF, refuses prediction
  language and fixture-profile markers in the report, and checks both the PDF's
  recovered text and its painted glyph IDs. A missing or refused PDF means
  incomplete delivery (exit 2); repair the cause and rerun before declaring
  completion.
- A redelivery returns to the same place and removes its own files it no longer
  produces. The hidden `.jobhunt-delivery.json` there records which workspace
  wrote each file; do not delete or edit it. Client files with no manifest entry
  (an older `deliver.py` recorded none) count as another workspace's unless they are
  byte-identical to this round's copies or the folder is this workspace's default
  `~/Downloads/<workspace-name>/`; the round then goes to a subfolder with
  `NOTICE_SEPARATE_FOLDER`. Quote both folders.
- In `discover`, `assess` and `interview`, an existing CV is source material, so
  delivery copies only the report by default. Use `--include-applications` only
  when the user explicitly asks to receive the existing application documents too.
  Do not regenerate or deliver a source CV merely because it is in the workspace.

## How this skill writes to the user

The CV and the letter have a gate for machine-sounding prose (`AI_VOCABULARY`,
`EM_DASH_DENSITY`, `NOT_JUST_PIVOT`, `TRICOLON_DENSITY` — `scripts/prose_tells.py`).
The documents this skill writes to the *reader* — `report.md`, `shortlist.md`,
`fit-assessment.md`, the completion message — have no mechanical style gate:
measured across all eight of them from the iteration-2 runs, the vocabulary check found
nothing and every structural finding was a false positive on a table or a list.
So the rules below are rules, not a check, and the artifact is the only place to
verify them. The sections above give the concrete revision method, examples and
final reader review, covering report structure and readability as well as
formulaic phrasing; they are not a blacklist or an AI-authorship detector.

- **Address the reader as "you", and say who said what.** "You told me you are on
  a search-year permit with eleven months left" is auditable; "the candidate has
  limited runway" is a summary of them written for someone else.
- **Every claim carries its evidence reference or its source line.** A row without
  one is an opinion, and the reader cannot object to one line of it.
- **Say the uncomfortable thing in the first sentence of its paragraph**, not
  after two of setup. "The advert says nothing either way about sponsorship" —
  then the consequence.
- **Name what was not done.** "No page was fetched live and no site was logged
  into for this assessment" costs one line and is the difference between a report
  and a claim.
- **No throat-clearing and no summary of the summary.** Do not open with "Great
  question", do not close by restating the table above it in prose, and do not
  offer to help further — the hand-off section already asks one specific question.
- **Plain words for hard things.** `recognised sponsor`, `kennismigrant` and
  `knockout` are terms the reader will meet in the real process, so use them and
  gloss them once. Everything else gets the ordinary word.
- **A tell you would flag in the candidate's letter is a tell in yours.** The
  vocabulary list in `prose_tells.py` applies to this skill's own prose too; it
  simply has no gate behind it here.
