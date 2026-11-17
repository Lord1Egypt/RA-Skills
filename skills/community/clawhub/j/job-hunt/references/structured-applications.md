# Structured / Competency-Based Applications

Some employers don't screen a free CV at all. They use a **structured application** where you must evidence each requirement explicitly, and the decision is made almost entirely on how well you map your experience to their stated criteria. The CV is secondary or absent; the real deliverable is a **supporting statement** written against the criteria. If you treat one of these like an ordinary CV application, the candidate scores near zero against the framework regardless of how good they are — the assessors literally tick boxes against criteria, and unaddressed criteria get no marks.

The big ones:
- **UK NHS** (NHS Jobs / TRAC): a person specification split into **Essential** and **Desirable** criteria across categories (Qualifications, Experience, Skills, Knowledge), plus a free-text **"Supporting Information"** box. Shortlisting scores each criterion against your statement.
- **UK Civil Service** ("Success Profiles"): **Behaviours** (e.g. "Making Effective Decisions", "Communicating and Influencing"), **Strengths**, **Experience**, **Technical/Ability** — with word-limited statements per behaviour, assessed with STAR.
- **Academic / research posts**, many **public-sector and university** roles, some **NGO/UN** systems (Inspira), and **government grad schemes** work the same way: address-each-criterion.

## How to detect it

Treat a posting as a structured application when the employer requests a
supporting statement, criterion-by-criterion evidence, a competency response or
a structured application form. Examples include "address each of the criteria",
"evidence how you meet", a statement scored against named criteria, or a
"supporting information" box with a word limit.

An **Essential / Desirable** split, "Person Specification" heading or framework
name alone describes requirements, not the documents to submit. If the employer
asks only for a CV, keep the CV route. If the requested material is genuinely
unclear, confirm it rather than silently replacing the CV with a statement.

When detected, **tell the user the deliverable is the supporting statement, not just the CV**, and confirm before proceeding — the CV may still be required as an attachment, but it won't be what wins the shortlisting.

## How to build the supporting statement

The statement is the primary artifact. Build it criterion-by-criterion so an assessor can find each tick.

1. **Extract every criterion verbatim** into a checklist — Essential first (these are scored hardest and an unmet Essential is usually an auto-reject), then Desirable. For Civil Service, list each named Behaviour and its word limit.
2. **For each criterion, write a short evidenced paragraph in STAR** (Situation, Task, Action, Result) drawn from the candidate's real experience — the same honest-reframing rules apply (`gap-analysis.md`): the evidence must trace to a real profile fact or a user answer this session. Lead the paragraph by echoing the criterion's own wording so the match is unmissable.
3. **Mirror the framework's structure and headings.** For NHS, group under the person-spec categories and put a sub-heading per criterion. For Civil Service, one section per Behaviour, each within its stated word limit (respect the limit exactly — over-limit statements are cut or penalised). **Word limits:** use the posting's stated limit when given; when none is stated, a useful default is ~100–200 words per criterion for NHS person-spec items and ~250 words per Civil Service behaviour — enough for a full STAR example without padding. Count and report length per section so the user can trim.
4. **Honest gaps are explicit.** If a Desirable criterion isn't met, it's fine to omit it or address it briefly with transferable evidence; an unmet **Essential** is a genuine fit problem — surface it to the user (the candidate may not be eligible) rather than papering over it.
5. **Run the same provenance checkpoint** as the CV: every claim of meeting a criterion cites a real source. **Distinguish an observable behaviour from a formal credential** — "applied information-governance policy" is evidenced by what the CV shows the candidate *did*; "completed information-governance training" is an HR credential the CV may not establish. Don't upgrade demonstrated behaviour into a claimed qualification — if a criterion asks for a specific certificate/training and the CV only shows related practice, flag it for the user to confirm rather than asserting it.

## Output

The deliverable is **Markdown** (and the candidate pastes it into the portal's free-text box — that is exactly how NHS Jobs and Civil Service Jobs collect it, so a plain, well-structured text document is the right and sufficient format). Write it to `<workspace>/supporting-statement.md`. There is no special renderer — clean Markdown with a heading per criterion is the artifact.

**Whether to also produce a CV:** make it only when the posting actually asks for one — check for a CV/résumé upload field or wording like "attach your CV". NHS Jobs typically does *not* take a free CV (the form replaces it); many Civil Service and academic posts do want one alongside. When it's ambiguous, produce the supporting statement (always needed) and ask the user whether a CV upload is also required, rather than silently producing or skipping it. When a CV is produced, make clear the statement is what gets scored.

**Record a confirmed statement-only route** in `<workspace>/application-plan.yaml`:

```yaml
application_type: structured
cv_required: false
source_ref: posting-source.md
source_quote: "Submit supporting information only; no CV attachment is accepted."
```

Copy the actual wording from the posting or the user's answer; the quote above is
an example, never evidence. `source_ref` must be a readable original input inside
the workspace: `input.md`, `posting-source.md`, `posting-source.txt`, or a file under
`raw/`, `inputs/`, or `source/`. Absolute paths, traversal and escaping symlinks are
not accepted. Both the plan and posting must say `application_type: structured`;
`cv_required` must be the YAML boolean `false`, not the string `"false"`.

The quote makes the routing decision reviewable. Its presence proves only that
the quoted text exists, not that its meaning justifies omitting the CV; read it
and resolve ambiguous upload instructions with the user. A missing plan keeps the
normal CV requirements. If any `cv.md`, `cv.docx`, `cv.pdf` or `cv.tex` is produced,
the CV still requires the three judges even when the plan says no CV was needed.
Keep the source and tailored profile for the ordinary provenance checks; omitting
a CV deliverable does not remove those checks. Follow the statement-only gate
sequence in `modes/apply.md` and record the criterion review there instead of
inventing CV judge verdicts.

```
# Supporting statement — <role>, <employer>

## Essential criteria

### <Criterion 1, in their words>
<STAR paragraph evidencing it with the candidate's real experience.>

### <Criterion 2 …>
…

## Desirable criteria
…
```

## Review

The CV judges (ATS / Recruiter / Hiring Manager) are calibrated to a free CV and an ATS pipeline — they don't model a criterion-scored form. So for a structured application, review the **supporting statement** against the framework instead: **every Essential criterion has a clearly-labelled, evidenced STAR paragraph; each statement is within any stated word limit; no criterion is unaddressed; claims are provenance-checked; unmet Essentials are surfaced honestly.** Report that criterion-coverage to the user (e.g. "8/8 Essential, 3/5 Desirable evidenced") in place of an ATS coverage %. If a CV is also required, run the normal judge loop on the CV as a secondary check.

**Read the statement for machine prose before you send it.** A criterion answer is 250 words written to persuade a human marker — the same register as a motivation letter, and the register where a model's habits are most visible. Because the CV judges are routed away from this branch, `scripts/check_word_limits.py` is the only reader this artifact has: it reports the 2026 vocabulary, the "not just X, but Y" pivot, em-dash density and tricolon density per criterion, so a finding names the answer to rewrite rather than the file. The tense matters here in a way it does not in a letter — a criterion answer describes work already done, so the construction usually arrives as "not just an audit **— it was** a chance to…". The gate covers that; `references/motivation-letter.md §6` carries the half no gate can measure, and it applies to a supporting statement unchanged.
