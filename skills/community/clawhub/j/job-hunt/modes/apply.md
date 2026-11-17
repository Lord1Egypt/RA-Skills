# Mode: apply

## Entry conditions

An assessment should exist. Its verdict decides how this mode opens, and only one
of the five stops it:

- `强烈建议投` / `值得投` — enter.
- `可以冲刺` (stretch) and `大概率被筛掉` (likely_screen_out) — **enter.** These do
  not block: building a solid application for a role the candidate is reaching for
  is not a defect, and refusing here would systematically underserve exactly the
  people this skill is for — stretch candidates and career switchers. Say the
  verdict out loud, then do the work well.
- `硬性阻断` (blocked) — **ask once**: "this is a legal-level barrier, not a
  phrasing problem — still want to apply?" If the user says yes, proceed and do the
  work properly. Ask once, not every step; a second ask is nagging, and a silent
  refusal is deciding for them.
- `证据不足—不出结论` (insufficient_evidence) — this is a refusal, not a level. Say what could not be read
  (the posting, the CV, an illegible region of an image source) and get that first.

No assessment at all is not a blocker either: run apply, and say plainly that no
fit assessment was made.

## On entering this mode

The workspace path is `paths.workspace(name, company, role, date)` (Step 4), so it needs
the company and role. As soon as you have them, create that directory and record the
entry, before writing any artifact into it — `check_apply.py` requires the record, and
the hash is what proves the file you read is the file on disk:

```bash
python3 scripts/paths.py --name "<meta.name>" --company "<company>" --role "<role>"   # prints <workspace>, absolute
python3 scripts/enter_mode.py --workspace <workspace> --mode apply \
    --because "<why apply, in one line, from what the user asked>"
```

Fingerprint the master once Step 1 has fixed which master and which CV language this
run uses (the end of Step 1 below).

## Fast path

**Fast path (reduce friction for the common case).** When the user already hands you a parseable CV *and* a clear posting (URL or pasted text) and is not building from scratch, do not gate every step with its own round-trip. Do the work, then present the parsed profile, the extracted requirements, and the tailoring plan **together in one message**, and proceed unless the user objects or corrects something. Still run every step and the non-negotiable three-judge review loop — this only collapses the *confirmation* round-trips, never the analysis or the judges. Reserve the full step-by-step interview for when information is genuinely missing (building a CV from scratch, an unreachable posting, or ambiguous requirements).

## Step 0 — Interview the user

Make a **single `AskUserQuestion` call** with up to 4 questions. Drop any question the user already answered in their opening request; keep the rest.

Use the host's supported question mechanism and limits. Never invent a missing
tool or use an unavailable interaction mode just to reproduce this example.

On a host without that tool — codex, another agent, or a Claude Code **subagent** — the requirement is the SHAPE, not the tool: ask the same questions in ONE message, each with lettered options. Never degrade to one question per turn. With no interactive user at all, state the assumptions you proceeded on and carry them into the completion message. See `references/portability.md`.

1. **CV source** — Do you have a CV to use, or should I build one for you? (If they choose *build*, follow up: can you share an example whose style I should mimic, or should I design a clean template?)
2. **Target region** — offer the three clusters (see `references/cv-craft.md §2`): **(1) Anglophone developed** (US, Canada, UK, Ireland, Australia, NZ), **(2) EU / EEA** (NL, DE, FR, BE, ES, IT, Nordics, …), **(3) East & SE Asia** (China, Japan, Korea, Singapore, Malaysia, Thailand), plus **Other**. The region options ARE these clusters — do **not** promote an individual country to its own top-level choice even when it is a returning user's saved default (e.g. the **Netherlands is offered *inside* EU / EEA**, never as a separate region). Once they pick a cluster, confirm the **specific country** (it refines length/photo/personal-data conventions) and the **CV language**: English for Cluster 1; **English or the official local language** for Clusters 2 and 3 (match the posting when unsure). Set `meta.target_market`, `meta.language`, and — for a non-built-in language — `meta.headings`. This drives formatting, content conventions, and the rendered language.

   **A saved profile is never an answer to this question.** `meta.target_market` records a
   previous application, and this field arms the personal-data interlock (a wrong market
   can put a photo or date of birth on a US CV, or strip the photo a German employer
   expects). Ask it every run, unless the market was explicitly confirmed for this target
   earlier in the current conversation. "Already answered" means answered *by the user, in this
   request*, never found in a file. Assess and interview also confirm the market under their own
   entry rules; a market already confirmed for this target in this conversation does not need to be asked again.
3. **Output formats** — Markdown / PDF / .docx (multi-select).
4. **Motivation letter** — Do you want a cover/motivation letter as well?

## Step 1 — CV acquisition → `profile.yaml`

Resolve the store with `scripts/paths.py` first. Paths below illustrate the default;
when `JOBHUNT_PROFILES_ROOT` is set, use `paths.PROFILES_ROOT` for profile and
resume lookups and report the actual saved paths. A missing store is normal on
first use; `save_profile.py` creates it when a profile is saved.

**Resume an in-progress application first.** Before anything else, check `~/.claude/job-profiles/*/applications/` for a workspace that matches this target (by company/role) and already contains a `posting.yaml` and/or `tailored-profile.yaml`. If one exists, a prior run was interrupted — show the user what's already there and offer to **resume from where it stopped** (e.g. posting already extracted → jump to gap analysis or tailoring) rather than rebuilding from Step 0. Only start fresh if they prefer it or no matching workspace exists.

**Check for existing profiles next.** Before building or parsing, check `~/.claude/job-profiles/` for any saved master profiles. If one or more exist, offer to reuse one (retargeting it for this new application) instead of rebuilding from scratch. A returning user can confirm a name and you jump straight to Step 2. New users with no saved profiles proceed to build/parse below.

**Reusing a master carries their experience forward, never their target.** `meta.target_market`, `meta.language` and any `contact.personal` in that file describe the application it was last built for. Re-ask the region and language (Step 0, question 2) before tailoring, and re-confirm any personal field the new market's cluster would treat differently — the master is the source of truth about the candidate, not about where they are applying.

The canonical profile schema is `assets/profile.example.yaml`. Everything downstream renders from a profile in this schema.

**If the user provides a CV** (file path or pasted text): parse it into the canonical schema. Show the parsed `profile.yaml` back to them and ask them to confirm or correct it before proceeding. Do not invent fields they didn't supply.

**If building from scratch:**
- If they gave a style example, mimic its structure and tone.
- Otherwise design a clean template guided by `references/cv-craft.md` (a light web search for current conventions is fine if useful).
- Either way, **interview the user section by section** — contact, summary, experience, education, skills, projects, etc. — until the profile is complete enough to render. Record only what they tell you; never fabricate.

**Enrich from linked artifacts, don't make the user retype.** When the profile names papers (titles/DOIs/arXiv) or links repositories (GitHub/GitLab), fetch and read them to extract concrete, truthful detail — what was built, the stack, scale, results, and the candidate's specific contribution — rather than asking the user to supply it. Use `WebFetch`/`WebSearch` (and the repo README / `gh` for GitHub). Only ask the user when the source is access-restricted (paywalled paper, private repo) or the fetch is blocked. Honest-only: extract the candidate's real contribution, never sole credit for a multi-author work. Full guidance: `references/gap-analysis.md §1` (Enrich from the candidate's papers and repositories).

**Offer to save the master** to `~/.claude/job-profiles/<name>/profile.yaml` so it's reusable across applications. This master profile is the source of truth and is **NEVER mutated by tailoring** — tailoring always works on a copy (Step 4).

**One candidate has one CV per language, and saving a new one never overwrites another language's.** A Chinese CV is a different document from an English one — different conventions, length rules and personal-data expectations — not a translation of it, so a user who supplies both has two masters: `profile.yaml` and `profile.<lang>.yaml` beside it. **Save through `python3 scripts/save_profile.py --name <name> --profile <file>`, never by writing the path yourself.** It resolves the slot by reading each existing master's own `meta.language` rather than trusting a filename, so a second English CV goes back into the legacy `profile.yaml` instead of becoming a duplicate; it backs up what it replaces; and it refuses a profile with no `meta.language`, because the unsuffixed slot is where a legacy English master usually lives and dropping an untagged CV there is the overwrite this is here to prevent. On the read side the same rule runs backwards: tailor from the master whose language matches the CV language chosen in Step 0, and say which file you took as the base. Reaching for the English master to build a Chinese CV throws away the one the user wrote for exactly that purpose.

**Before fingerprinting, run the online-presence step**
(`references/online-presence.md`): `python3 scripts/online_presence.py status --name
"<name>" --workspace <workspace>`, ask once for anything it lists, check and confirm
findings, then `writeback`. Confirmed public work (a repository the CV omits) then
reaches this run through the master, as an ordinary `profile-line` source.

**Then fingerprint that master.** The path comes from `scripts/paths.py` and takes the CV
language, because one candidate can have one master per language; without it this
resolves to `profile.yaml` and the provenance gate checks a Chinese CV against an
English master:

```bash
python3 scripts/check_claims.py --workspace <workspace> \
    --master "$(python3 -c "import sys;sys.path.insert(0,'scripts');import paths;print(paths.master_for_language('<name>', '<cv language>'))")" \
    --record
```

## Step 2 — Job posting → structured requirements

Read `references/job-posting-extraction.md` and follow it.

- Try `WebFetch` on the posting URL.
- **Sanity-check the fetched content before extracting.** Many portals (LinkedIn / Workday / Greenhouse / Indeed) return a `200 OK` that is actually a login wall, cookie banner, or error page — not the posting. If the fetched text lacks recognizable posting structure (no responsibilities, no requirements, looks like a sign-in/search page), treat the fetch as **failed** — do not extract requirements from a login wall (you'd fabricate must-haves). Ask the user to paste the full posting text instead.
- If the fetch is blocked or thin, ask the user to paste the full posting text. **Terminal behavior:** if no posting can be obtained at all (URL dead, user can't paste), stop gracefully and say so — never invent a posting or proceed on guessed requirements.
- Extract the structured object — **all twelve names, in this order**, the same list
  as `references/job-posting-extraction.md`'s extraction field table and `modes/assess.md` §3:
  `role_title`, `company`, `seniority`, `location`, `must_haves`, `nice_to_haves`,
  `responsibilities`, `keywords`, `company_values_tone`, `red_flags`, `salary_range`,
  `application_type`.
- **Detect a structured / competency-based application.** Use `structured` when the employer requests a supporting statement, criterion-by-criterion evidence, a competency response or a structured application form. Essential / Desirable headings or a framework name alone do not change a CV application into a statement. Read `references/structured-applications.md`, confirm any genuinely ambiguous requested document, and preserve an explicitly requested CV alongside the statement.
- **Confirm the must-haves and keywords with the user** before moving on.
- After confirmation, write the extracted and confirmed posting to `posting.yaml` in the application workspace (defined in Step 4 below). This persists the posting for re-runs and the user's records.

## Step 3 — Gap analysis

Read `references/gap-analysis.md` and follow it.

- Build the **strong / partial / missing** table comparing the profile to the requirements, each row backed by evidence from the CV.
- **Run the responsibility-evidence pass** (`gap-analysis.md §1`): for each of the posting's `responsibilities[]`, classify the candidate's strongest real evidence `demonstrated / adjacent / none`. This aligns the CV to the *day-job*, not just the requirements checklist — a `demonstrated` responsibility buried in the CV becomes a LEAD-WITH instruction; a `none` on a core responsibility is a real fit gap to surface.
- **Record the before-tailoring FIT SNAPSHOT in internal `fit-snapshot.md`** (`gap-analysis.md` §4, "FIT SNAPSHOT"): must-have coverage ("X of N strongly evidenced" + per-must-have table), responsibility match ("M of K core responsibilities demonstrated"), and the seniority/domain read in one line each, ending with an honest **apply verdict** (strong apply / worth applying / stretch / likely screen-out / blocked). Include the required disclaimer (a count of evidence, not a forecast of the outcome). Use it to explain the meaningful before/after changes in the client report, without copying the internal count block.
- Present the **tailoring plan** as the four lists: **AMPLIFY / REFRAME / KEYWORD-INSERT / HONEST-GAPS**.
- **Non-standard candidate?** If the profile shows an employment gap >6 months, a domain/function switch vs. the posting, a seniority mismatch (over- or under-leveled), an extended absence/re-entry, very thin experience (student/new-grad), a **senior-leadership/executive** profile, a **military-to-civilian** transition, or an **internationally-trained/relocating** candidate, read `references/candidate-situations.md` and apply the matching honest-positioning playbook **before** building the tailoring plan. These are the candidates the skill helps most.
- **Non-technical or regulated role?** If the target is not a software/research/engineering job (e.g. clinical, sales, trades, legal, finance, public-sector, creative, teaching, hospitality), read `references/role-families.md` and apply that family's conventions — what to surface first and how competence is evidenced — when shaping the tailoring plan and section order. The metric-in-every-bullet default doesn't fit these; the qualitative-evidence rule in `gap-analysis.md §2` does.
- Where a gap might be closed with information the CV merely omitted (not invented), ask the user **targeted supplementary questions**. Honest only — never phrase a question as an invitation to fabricate.
- **Claim-provenance checkpoint (mandatory before writing any tailored content):** Every new skill, tool, scope, or technology claim introduced via REFRAME or KEYWORD-INSERT must trace to either (a) a specific line or field in the candidate's source profile, or (b) an answer the user gave during this session when asked a supplementary question. If neither source exists, the claim does NOT enter the CV — place it in HONEST-GAPS instead. See `references/gap-analysis.md` (claim-provenance checkpoint) for the full rule.

## Step 4 — Tailor the CV

**Application workspace.** All per-application files live under:

```
~/.claude/job-profiles/<name>/applications/<company>-<role>-<YYYY-MM-DD>/
```

This workspace contains: `tailored-profile.yaml`, `letter.yaml` (if any), `posting.yaml`, and the rendered outputs (`cv.md`, `cv.docx`, `cv.pdf`, `letter.*`). The master profile at `~/.claude/job-profiles/<name>/profile.yaml` is **NEVER** mutated.

### `claims.yaml` — write it as you tailor, not afterwards

The checkpoint in Step 3 is enforced by `scripts/check_claims.py`, and the ledger
it reads is `<workspace>/claims.yaml`. **Append a row at the moment you write each
REFRAME or KEYWORD-INSERT.** A term in the tailored CV that is neither in the
master profile nor sourced by a row here is `UNSOURCED`, and `check_apply.py` will
not let the package be delivered over it. A title that lost a subordinate-rank word
(`Assistant Manager` → `Manager`), a status marker (`(in progress)`) or a publication
status (`(under review)`, `(submitted)`, `preprint`, 审稿中) is
`QUALIFIER_STRIPPED`, and an employer or institution shortened into a different name
is `ORG_TRUNCATED`, and a title, degree or project role copied from a different entry of
the master (an earlier `Analyst` role relabelled with a later role's `Data Scientist`) is
`TITLE_FROM_OTHER_ENTRY`; all three block delivery the same way. Restore the real wording; a
claims row is only for a genuine, sourced equivalence.


```yaml
- term: PACS export                       # the exact string as it appears in the CV
  where: cv.md:experience[0].bullets[1]   # artifact and place it was inserted
  source_kind: session-answer             # profile-line | session-answer | fetched-artifact
  source_ref: mock/transcript-2.md#Q1     # a real path under the workspace, or a profile field
  session_date: "2026-08-09"              # YYYY-MM-DD
  retracted: null                         # null while live; true once withdrawn
```

- **All six keys on every row.** `retracted` is required even when null: in a
  schema where "absent" and "not retracted" look the same, a withdrawn claim
  leaves no scar, and the scar is why the field exists.
- **Three source kinds, and there is no fourth.** `profile-line` (already in
  `profile.yaml` — the ordinary case), `session-answer` (the candidate said it,
  in a recorded session), `fetched-artifact` (a paper, repo or page this run
  fetched).
- **Append-only.** A claim that turns out to be wrong is marked
  `retracted: true`, never deleted. A retracted row stops being a source:
  `check_mock.py` refuses to let it discharge an `UNSOURCED-FACT`.
- `source_ref` must resolve. For a `session-answer` row, `check_mock.py` requires
  it to name a file that exists under the workspace **and** to contain the term.

A worked file, including a retracted row, is in `assets/claims.example.yaml`.

- Write the tailored copy to `<workspace>/tailored-profile.yaml`. **Never edit the master.**
- Apply the tailoring plan: reorder, re-emphasize, weave in exact keywords **where truthful**, and trim to the market's length conventions (see `references/cv-craft.md`).
- **User template takes precedence:** when the user supplies a reference CV/template, inspect its actual section, entry and bullet order before tailoring. Preserve that order in all rendered formats. Set `meta.section_order` and `meta.headings` from it, remove an unrequested generated summary if the template has none, and mark internship entries with `experience[].section: internships` when they have their own section. Preserve entry and bullet order in the profile arrays; do not reorder them using career heuristics. Compare the generated DOCX/PDF headings and entry sequence to the reference before delivery. The following default order advice applies only when no user template specifies the order.
- **Section order:** confirm the order fits the candidate and target (`cv-craft.md §1`, **including its 'Deciding between the templates' block** — read it whenever the candidate matches more than one template, which a PhD applying to industry always does). The renderer auto-leads with Education for a current PhD/researcher (or a no-experience student) and with Experience for everyone else; when that's wrong for this application, set `meta.section_order` explicitly in the tailored profile. **What decides it is how RELEVANT the degree is to the target role, not whether the employer is academic or industrial.** A doctorate in the role's own field is a credential the reader is looking for and belongs near the top whoever the employer is; an industry engineering target leads with Experience even for a PhD *only when the doctorate is not in that role's domain*, or once the candidate has 3+ years of formal experience. Academic/research targets lead with Education and surface Publications early. Say which template you applied and offer the alternative — this is the candidate's call to make.
- **Projects vs. Experience (de-duplicate):** work done inside a job belongs as bullets under that role, not restated in a separate Projects section; Projects holds only genuinely standalone work (thesis, coursework, open-source, competitions). Cut a Projects section that merely echoes the day job or lists stale coursework. See `cv-craft.md §9`.
- **Links:** keep links in `contact.links` keyed by service (`scholar`, `github`, `linkedin`, …) so the renderer shows a clean label ("Google Scholar", "GitHub") hyperlinked to the URL — never the raw URL as visible text. Use the `{label, url}` form for anything unusual. See `cv-craft.md §8`.
- **Bullet-quality pass:** After tailoring, run a quick pass over every bullet — each should open with a strong action verb, carry a real metric/scope/outcome where truthful, and be **concise (one line ideally, two at most; front-load the point; cut filler words)** so a skimming recruiter reads it. Strip clichés ("results-driven", "proven track record", "synergy", "leveraged"). For bullets lacking a number, apply the quantification fallback ladder from `references/gap-analysis.md §2`. Honest-only still applies — do not invent metrics. See `cv-craft.md §3` for the conciseness rule.
- **AI-uniformity pass:** Run the full-CV coherence check from `references/gap-analysis.md` (post-tailoring AI-uniformity check): verb variety, sentence-structure variety, voice and specificity, prose quality. Make targeted repairs before delivering. The goal is a CV that reads as one human's real work history, not a keyword-filled template. `lint_cv`, `check_letter` and `check_word_limits` report the mechanical half (`AI_VOCABULARY`, `EM_DASH_DENSITY`, `NOT_JUST_PIVOT`, `TRICOLON_DENSITY`) — treat a clean run as the floor, not as the pass: no gate can see that three roles were written to the same template.
- **Update the internal after-tailoring FIT SNAPSHOT** (same format as Step 3 — coverage, responsibility match, apply verdict) to record the delta. Keep the same disclaimer in the internal record.
- **File-format note:** For ATS/portal submission, `.docx` is the safer default (see `references/cv-craft.md §4`). PDF is for the human-facing copy or when explicitly requested by the posting. If the portal gives a choice and the posting doesn't specify, submit `.docx`.
- Render Markdown and DOCX from the tailored profile, adapting the DOCX to the
  selected reference first. Export the **final DOCX** with Word/LibreOffice into
  `raw/layout/word-export.pdf`, then copy that export to `cv.pdf`. Inspect both
  final formats. Keep the export and its source DOCX hash in `layout-review.yaml`.
  Do not separately generate a LaTeX CV PDF when delivering the matching Word/PDF pair.
  Word prose must not contain Markdown or LaTeX source. Follow
  `references/word-resume-layout.md` to repair notation in the tailored copy;
  `DOCX_MARKUP` requires correction, a fresh render/export and another review.
  The renderer supports these individual formats:

  ```bash
  python scripts/render_cv.py <workspace>/tailored-profile.yaml --format <md|docx|pdf> --out <workspace>/cv.<ext>
  ```

- **For an explicitly requested standalone LaTeX PDF**, `--format pdf` writes
  `cv.tex` next to `cv.pdf`; deliver its `.tex` source too. Word-exported PDFs do
  not need a `.tex` file. The following engine troubleshooting applies only to
  the LaTeX route; its output must still satisfy the selected format requirements.
- If the PDF run warns about a missing LaTeX engine: follow `references/agent-setup.md` to install a suitable engine, then re-render and verify the requested PDF. If setup is blocked, deliver the available Markdown, .docx and `.tex`, and name the actual blocker. The renderer's no-engine fallback exits 0; that does not mean a PDF was produced.
- If `HOST_EXECUTION_REQUIRED` appears, the engine is installed but the current restricted process cannot reach a required host service. Follow `references/agent-setup.md` to rerun only rendering and PDF verification through the host's approved trusted or elevated route. Do not reinstall the engine, substitute an old PDF, or mark the PDF delivered until that rerun passes.
- **If the PDF run exits non-zero and reports dropped characters, there is no PDF and there must not be one.** The engine reports a `Missing character` per glyph it could not typeset and still exits 0 by itself, so the renderer scans for them and refuses; `cv.md` and `cv.docx` are unaffected and will look perfect while the PDF would have lost letters out of the candidate's own name. Do not hand over a PDF from a previous run, and do not describe the PDF as delivered. Read the codepoints it names, set `meta.main_font` (Latin) or `meta.cjk_font` (CJK) in the tailored profile to a font installed on this machine, and re-render — or ship `.docx` + `.tex` and say plainly that the PDF could not be produced.
- **Japan rirekisho fork:** if the target is Japan AND a traditional/domestic employer (or the user asks for a 履歴書), the standard form differs from the Western CV — render it with `scripts/render_rirekisho.py` per `references/rirekisho.md`. Collect the `jp:` personal-data fields honestly from the user (DOB, address, photo, furigana, 志望の動機 — never invent them), compute `age` from DOB using today's date, output `.docx` (the authentic form; export to PDF from Word/LibreOffice), and keep the Western CV as the companion 職務経歴書. For an international/foreign-capital employer, the normal Western CV (Step 4 above, in Japanese or English) is correct — don't force a rirekisho.

  ```bash
  python scripts/render_rirekisho.py <workspace>/tailored-profile.yaml --format docx --out <workspace>/rirekisho.docx
  ```

## Step 5 — Motivation letter (if requested)

Read `references/motivation-letter.md` and follow it.

- **Skip gate (apply before drafting):** Per `references/motivation-letter.md §0`, check whether a letter is actually needed. If the portal has no field for it, the posting says to skip it, it is a high-volume/quick-apply role where letters are not standard, or a strong referral has effectively replaced it — say so and skip rather than forcing a letter. Only proceed if a letter is genuinely warranted.
- Draft the letter into `<workspace>/letter.yaml` with this exact schema:
  - `meta`: `{language, target_market}` — copied from `tailored-profile.yaml`'s `meta`, so the letter is in the CV's language and on the CV's paper size
  - `sender`: `{name, email, location}`
  - `recipient`: `{name, company, location}`
  - `date`
  - `salutation`
  - `body`: list of paragraph strings
  - `closing`
- Render in the requested formats:

  ```bash
  python scripts/render_letter.py <workspace>/letter.yaml --format <md|docx|pdf> --out <workspace>/letter.<ext>
  ```

- Same honest rule and same LaTeX-fallback note as Step 4.

## Step 6 — Hiring-pipeline review loop (non-negotiable)

**Layout review is mandatory before the content judges and after any re-render.**
Read `references/layout-review.md`. Open every final Word/PDF page and compare
it with the actual user-supplied template, honoring the user's later changes.
Check fonts and sizes, page geometry, full-width heading rules, date alignment,
paragraph spacing, section/entry/bullet order, and pagination/clipping. A matching
section order or a readable PDF alone does not establish template fidelity.
Fix unapproved differences before delivery. Record the comparison, template and
final-file hashes, and inspected page previews in `layout-review.yaml`; run
`python scripts/check_layout.py --workspace <workspace>`. `check_apply.py` requires
its current passing receipt whenever a Word or PDF CV exists. Keep this record
in the workspace; the client receives their CV and career advice, not this audit.

**Three independent judges** must **all** return `PASS` before the package is interview-ready. They model the real hiring funnel — **ATS → Recruiter/HR → Hiring Manager** — and fail in *different* directions, so the CV must be **machine-findable, recruiter-skimmable & eligible, and genuinely strong** to clear all three:

**This is an actor–critic loop.** Each round: the three critics judge **in parallel** (one message, three `Agent` calls); if any rejects, the **actor — you, the orchestrator — applies targeted edits** addressing only the flagged points, re-renders, and re-judges **all three**. The actor stays inline (not a separate subagent) because it already holds full context and is the only party that can ask the candidate honest supplementary questions. **Stop the moment all three pass (early exit — often round 1).** The speed comes from parallel critics + targeted edits, not from spawning more agents. (Conceptually the funnel is sequential — ATS gates first — but requiring *all three* to pass yields the same end state, so run them concurrently.)

- **ATS Screener (machine lens)** — `agents/ats-screener.md` — text-matchable must-have coverage and parse/format sanity on the CV only; preserve values/motivation and explicitly future-dated eligibility in `NON_KEYWORD_REQUIREMENTS` for human review. Output: `VERDICT`, `COVERAGE`, `NON_KEYWORD_REQUIREMENTS`, `MISSING_OR_WEAK`, `FORMAT_ISSUES`, `TOP_FEEDBACK`.
- **Recruiter / HR Screener (fast human screen)** — `agents/recruiter-screener.md` — fast-skim must-have fit, readability, written communication, **logistics/eligibility** (location, work authorization, seniority band, salary), and targeting. The broad first human pass. Output: `VERDICT`, `SCORES`, `SCREEN_NOTE`, `TOP_FEEDBACK`, `SUPPLEMENTARY_QUESTIONS_FOR_CANDIDATE`.
- **Hiring Manager (deep human lens)** — `agents/hiring-manager.md` — real fit, seniority/leveling, evidence/credibility, clarity, narrative coherence, the standout signal, and (if present) the cover letter's authenticity. Output: `VERDICT`, `SCORES`, `LEVELING`, `STANDOUT_SIGNAL`, `TOP_FEEDBACK`, `SUPPLEMENTARY_QUESTIONS_FOR_CANDIDATE`.

The three lenses are deliberately distinct: ATS = literal findability, Recruiter = fast/broad/logistics, Hiring Manager = deep technical fit. Some overlap is expected; each owns its lane (the agent files state the boundaries).

**Dispatch all three in parallel** — as fresh independent **Agent** subagents in a **single message (three tool calls at once)** each round, so they run concurrently. They share no state, so parallel dispatch is both faster and avoids ordering bias; never run one, read its verdict, then run the next. Each has **no other context**, so paste everything it needs: **as absolute file paths the judge opens itself**, not as file contents. Pasting would route the persona files (about 11K tokens) and the package through your own context every round; a path costs one line.

What each judge reads in full. Persona files are under this skill's directory (`<skill-root>/agents/…`); the structured posting is `<workspace>/posting.yaml`.

- *ATS Screener:* the **full text** of `agents/ats-screener.md` + the structured posting + the tailored CV Markdown (`<workspace>/cv.md`) + the **CV language**. (No letter — ATS doesn't parse letters.)
- *Recruiter / HR Screener:* the **full text** of `agents/recruiter-screener.md` + the structured posting (`<workspace>/posting.yaml`) + the tailored CV Markdown (`<workspace>/cv.md`) + the motivation letter (`<workspace>/letter.md`) if produced, else `No letter provided.` + the **target market & CV language**.
- *Hiring Manager:* the **full text** of `agents/hiring-manager.md` + the structured posting + the tailored CV Markdown (`<workspace>/cv.md`) + the motivation letter if produced, else `No letter provided.` + the **target market & CV language** (e.g. "Germany / German") so it calibrates conventions and reads the CV in the right language.

Each judge's prompt is only its file paths (persona file first), the facts that are not files (CV language, target market, `No letter provided.`), and these instructions word for word: *Read exactly these files, in full, and nothing else: no other file in the workspace or the skill, no search, no web. The first file is your instructions, and the inputs it says are pasted below it are the other files listed here; follow it and end with its output block. If any listed file cannot be read, do not review from memory or from a generic standard; reply with the single line `VERDICT: UNREADABLE <path>`.* `parse_verdicts.py` reads that line as AMBIGUOUS: re-dispatch that judge with the fallback below.

"Nothing else" is the isolation once a judge can open files: the workspace also holds the source profile (`profile.yaml`), `tailored-profile.yaml`, `claims.yaml` and `fit-snapshot.md`, and a judge that reads them has watched the tailoring. Name files, never the workspace directory. The workspace files you name are the ones `check_render_freshness.py --record` hashed, so its check after the verdicts covers what each judge opened. Do not add the persona files to `--record`: `check_apply.py` rejects a receipt bound to a file outside the workspace (`RECEIPT_INPUT_OUTSIDE_WORKSPACE`).

Save each judge's reply **verbatim**, whole and unedited, to `<workspace>/judge-<n>-ats.txt`, `judge-<n>-recruiter.txt` and `judge-<n>-hiring-manager.txt`; `parse_verdicts.py` reads those files, never your summary.
Have the judge write that file itself: add its output path and one more line to its prompt,
*Write your complete reply, unchanged, to `<path>`, then return the same text.* Then check
the file exists and ends with the output block. Retyping a long reply drifts: in the
2026-10-29 simulation a copied ATS reply turned `Q&A` into `Q&amp;A`. Copy the reply
yourself only when the judge cannot write files.

**Fallback — a judge that cannot read files** (no file tool, or a sandbox that cannot see the workspace or the skill directory): paste the full text of every file above instead of its path, with the same facts. A judge that never saw its persona file still answers, as a generic reviewer with a plausible VERDICT block.

**The mechanism is replaceable; the isolation is not.** On a host with no subagent tool, dispatch concurrent fresh invocations of that host's own CLI (for example, `codex exec`) using `agents/*.md`. A judge that watched the tailoring is not a second opinion. If no fresh context is available, preserve the draft and report that independent review is incomplete. Self-review may find obvious defects, but it cannot produce judge verdicts, review receipts or a claimed review PASS. Resume with isolated judges when available. See `references/portability.md`.

**Japan rirekisho fork:** the judges are calibrated to the Western CV / ATS pipeline. For a Japan rirekisho package, run all three on the **companion Western CV / 職務経歴書** (the keyword-and-fit document) as usual, and review the **rirekisho form itself** with the completeness/correctness check in `references/rirekisho.md` (required fields present, 学歴・職歴 chronological and gap-explained, no fabricated personal data) — report that to the user instead of an ATS coverage %. Do not feed the rirekisho `.docx`/`.md` to the ATS screener.

**Parsing each verdict (apply exactly, to all three):**

1. In each judge's response, find the last line beginning with `VERDICT:` followed by `PASS` or `REJECT` (case-insensitive). If absent or ambiguous (anything other than exactly `PASS`/`REJECT`), treat that judge as `REJECT` and re-dispatch it.
2. ATS Screener: also read `COVERAGE`, `NON_KEYWORD_REQUIREMENTS`, `MISSING_OR_WEAK`, and `FORMAT_ISSUES`. Verify every original must-have is either keyword-scoped or explicitly retained for human/by-start review. A high keyword count does not clear an unresolved qualification, and an absent values slogan is not a reason to add ungrounded self-praise.
3. Recruiter / HR Screener: also read `SCORES`, `SCREEN_NOTE`, `TOP_FEEDBACK`, and `SUPPLEMENTARY_QUESTIONS_FOR_CANDIDATE`. The recruiter's questions are often **logistics** (work authorization, relocation) — surface them to the user.
4. Hiring Manager: also read `SCORES`, `LEVELING`, `STANDOUT_SIGNAL`, `TOP_FEEDBACK`, and `SUPPLEMENTARY_QUESTIONS_FOR_CANDIDATE` (a single `  - none` bullet means no questions). `LEVELING` and `STANDOUT_SIGNAL` are advisory — they do not change the verdict, but relay them to the user and act on them when tailoring (e.g. lead the summary with a buried standout signal; address an under-leveled read).

**Combined verdict: PASS only if ALL THREE judges return `PASS`.** If any is `REJECT`, the round is a `REJECT`.

**If `REJECT` — per-round sequence (order is mandatory):**

1. **Edit first (targeted):** Merge the `TOP_FEEDBACK` from all three judges (plus the ATS `MISSING_OR_WEAK` / `FORMAT_ISSUES` and the Recruiter's logistics/readability flags) and apply edits that address **only the flagged points** — do not re-tailor sections the judges didn't fault. Apply to `<workspace>/tailored-profile.yaml` (and `<workspace>/letter.yaml` if present). Ask the user any `SUPPLEMENTARY_QUESTIONS_FOR_CANDIDATE` from the Recruiter or Hiring Manager — honestly, never inviting fabrication. **A keyword the ATS screener flags as missing goes into the CV ONLY if the candidate genuinely has it** (the claim-provenance checkpoint still applies); otherwise it stays in HONEST-GAPS. **Re-run the claim-provenance checkpoint on every edit made this round before re-rendering** — any term added to satisfy an ATS REJECT must cite its source (a profile line or a user answer this session). The correct response to an ATS gap you cannot honestly close is to let the loop fail at round 3 and report it — *never* to insert an ungrounded keyword. A coverage gate failing because the candidate genuinely lacks must-haves is a true result, not a problem to engineer around.
2. **Re-render second:** Re-render ONLY the affected outputs from the just-edited YAML (never re-send stale rendered files).
3. **Re-judge third:** Dispatch all three fresh judges with the newly rendered files. Never re-dispatch with the old rendered version.

**Honest-gap early-stop (don't grind a loop you cannot win honestly).** After any round, diagnose *why* a judge still rejects before spending another round:
- If the **only** remaining cause is must-haves the candidate **genuinely lacks** — terms the claim-provenance checkpoint forbids you to add — then no honest edit can move that number. Looping again would only pressure you toward the one thing the skill forbids (inserting an ungrounded keyword). **Stop now**, even before round 3, and report it as an honest gap, not a failure of the package. This is the *expected* outcome for a genuine stretch application, and it is a true result — surface it, don't engineer around it.
- Keep iterating only while the rejects are about things you *can* honestly fix: ordering, emphasis, surfacing a buried real qualification, readability, missing logistics notes, a real keyword the candidate has but the CV omitted.

**Loop until ALL THREE pass, the honest-gap early-stop fires, or 3 rounds** (early-exit the instant all three pass — don't run extra rounds). If not all passed, **STOP** and report honestly — but **distinguish the two very different reasons a package can end un-passed**, because they mean opposite things for the user:
- **Poorly built** — a judge rejects over something fixable that tailoring should have caught (weak ordering, vague bullets, an unaddressed logistic, a real-but-hidden qualification). This is a tailoring miss to own and, budget permitting, fix.
- **Honest stretch** — the package is as strong as it can truthfully be, and the only thing keeping a `>= 4` deep-fit gate from passing is that the candidate is genuinely a notch off the role (the Step 3 apply verdict was "stretch"/"worth applying"). This is **not** a defective application: it is a well-built application for a reach role, and the user may well still submit it. Say so plainly — "this is a strong submission for a stretch; the gap is real and the honest framing is X" — rather than reporting a bare "failed review."

In both cases give the final per-judge verdicts, the ATS coverage % (or `n/a`), the remaining honest gaps, and concrete next steps (skills to gain, certifications, better-fitting roles). **Never fake a pass.**

Tell the user **all three verdicts and the ATS coverage %** (report it verbatim — it may be `n/a`, e.g. a rirekisho or a posting with no extractable must-haves) each round.

## Step 7 — Finalize

- Link the actual client delivery folder and each requested document after `deliver.py` succeeds. Keep the workspace, `.tex` sources and review records private unless the user explicitly asks for them. Do not present an internal source as a finished client document.
- Record the **final FIT SNAPSHOT delta** internally, then explain the decision and changes in plain client language: baseline (before tailoring) vs. final (after tailoring) — coverage, responsibility match, and the apply verdict.
- Summarize what changed during tailoring and why.
- Note any **remaining honest gaps** the user should be aware of going into the application and interview.
- If `check_apply.py` emits `NO_ASSESSMENT`, say plainly in the final reply that no separate fit assessment was made. The apply-mode FIT SNAPSHOT and CV judge verdicts do not constitute that assessment.
- **Consistency reminder:** the tailored CV now states specific things about the candidate's roles, scope, and dates. Remind them to make sure their **LinkedIn and any portal profile don't contradict it** — recruiters cross-check, and a mismatch reads as dishonesty. (A reminder only — do not scrape or fetch their profile.)
- If a reusable **master profile** was saved, mention its actual path and that it can be reused for the next application. Never claim a default path was created without verifying it.

### Step 7.5 — Interview-readiness brief

Produce the brief in `references/interview-prep.md` (write it to `<workspace>/interview-brief.md`). Use the claim-provenance map, the judges' `SUPPLEMENTARY_QUESTIONS_FOR_CANDIDATE`, and the HONEST-GAPS. For each REFRAMED/AMPLIFIED claim, give the source fact and a "be ready to explain…" prompt; for each honest gap, the truthful framing if asked; and carry over the recruiter/manager questions. If a claim cannot be truthfully defended, walk it back on the CV and re-run the affected checks.

Keep the rendered brief to **one page or less**. If delivery reports `INTERVIEW_BRIEF_TOO_LONG`, condense repeated wording while retaining the claim sources, honest gaps and reviewer questions, then render and inspect it again. Do not shrink the text to force it onto one page.

After a mock interview, the complete structured `## Walk-back list` may follow as an appendix in the same Markdown/PDF. The quick-reference body must still fit on the actual PDF's first page; keep all walk-back records intact and put no further quick-reference sections after the appendix.

### Step 7.6 — Offer what comes next

Apply ends here, and the user is now at the point the other three modes exist
for. **Ask which they want, in one `AskUserQuestion` with selectable options —
and run none of them unasked** (`SKILL.md`, "The load-bearing rule"):

- **`interview`** — rehearse this package and debrief it. The natural next step:
  the CV now makes specific claims, and the mock round is where the candidate
  finds out whether they can defend them under one follow-up.
- **`assess`** — judge another posting before building for it.
- **`discover`** — find more roles worth looking at.

Offer only modes whose inputs exist, and say plainly if the loop ended
un-passed: a `blocked` or `honest_stretch` package makes `interview` more useful,
not less, because the gaps are known going in.

## Toolchain note

This note concerns template-based CV/letter rendering. Run the private setup in
`references/agent-setup.md` and use its recorded interpreter; it also installs
PyMuPDF. Consultation report PDFs use bundled fonts and do not require TeX.

- Scripts need their dependencies: `pip install -r requirements.txt` (PyYAML, python-docx).
- Standalone LaTeX PDF output needs a LaTeX engine — `tectonic` is recommended. Without it, **Markdown and .docx still work**, and the renderer emits a `.tex` file you can compile later.

## Gate commands, in the order they run

**Confirmed statement-only structured applications:** first write the sourced
`application-plan.yaml` described in `references/structured-applications.md`.
Keep `profile.yaml`, `tailored-profile.yaml` and the claim ledger for provenance,
but do not render a CV when the confirmed portal instructions exclude it.
Run `check_personal_data` and the verifying `check_claims` pass as usual, then
`check_word_limits`. Replace the CV dispatch block below with:

```bash
python3 scripts/check_render_freshness.py --workspace <ws> --round 1 \
    --record <ws>/supporting-statement.md <ws>/posting.yaml \
    <ws>/application-plan.yaml <ws>/<source_ref>
# Read the statement against every Essential criterion; verify evidence and
# STAR structure, record the criterion coverage and any honest gaps in the
# completion report, and prepare interview-brief.md. No CV judge verdicts.
python3 scripts/check_render_freshness.py --workspace <ws> --round 1
python3 scripts/check_apply.py --workspace <ws>
```

The final gate still requires the statement, its word-limit check, provenance,
and freshness of the statement, posting, plan and quoted source. A missing plan
does not activate this exception; producing any CV restores the normal three-judge
loop. For structured applications that also require a CV, use the full block below
and separately review the supporting statement against its criteria.

```bash
# after tailoring, before dispatching the judges
python3 scripts/check_personal_data.py --workspace <ws>
python3 scripts/check_claims.py --workspace <ws>
python3 scripts/lint_cv.py --workspace <ws>
python3 scripts/check_letter.py --workspace <ws>          # required once letter.yaml exists
python3 scripts/check_pages.py --workspace <ws>           # required once cv.pdf exists
# Also exports any cv.docx / letter.docx through LibreOffice and checks their pages.
python3 scripts/check_word_limits.py --workspace <ws>     # required once supporting-statement.md
                                                          # exists — and for a structured
                                                          # posting that has none, which is
                                                          # a missing deliverable, not a skip
python3 scripts/check_render_freshness.py --workspace <ws> --round <n> \
    --record <ws>/cv.md <ws>/posting.yaml <ws>/letter.md  # letter.md only if produced

# ... dispatch all three judges in parallel, save each reply verbatim ...

python3 scripts/parse_verdicts.py --workspace <ws> --round <n> \
    --ats <ws>/judge-<n>-ats.txt --recruiter <ws>/judge-<n>-recruiter.txt \
    --hiring-manager <ws>/judge-<n>-hiring-manager.txt
python3 scripts/check_render_freshness.py --workspace <ws> --round <n>
# ... at the end of the mode ...
python3 scripts/check_apply.py --workspace <ws>
```

**Run each verifying pass after the last `--record` for that gate**: a `--record` receipt
says `baseline_recorded` and `check_apply.py` reports it as `NOT_VERIFIED`. It also
fails on any gate whose latest receipt is `fail`. **Every round re-runs the whole
pre-dispatch block** after any edit (`check_personal_data`, `check_claims`, `lint_cv`,
and `check_pages`/`check_letter`/`check_word_limits` where they apply); otherwise
`check_apply.py` reports `STALE_RECEIPT` at the very end.

## `honest-stop.yaml` — required whenever the loop ends without a PASS

The three-judge loop ending un-passed means one of two opposite things, and they emit
the identical machine signal. Writing this file is how the run says which:

```yaml
classification: honest_stretch     # honest_stretch | poorly_built
verdict: stretch                   # strong_apply | worth_applying | stretch |
                                   # likely_screen_out | blocked
reason: >-
  The package is as strong as it can truthfully be. The only unmet must-have is
  five years of clinical PACS integration, which the candidate genuinely lacks.
evidence:                          # the judge findings the classification rests on
  - "hiring_manager requirement_match: 3/5 — no clinical PACS work"
  - "ats COVERAGE: 78% (7 present, 1 partial of 9 must-haves)"
```

- `honest_stretch` — the package is as strong as it can truthfully be and the candidate
  is genuinely a notch off the role. **Not** a defective application: say so plainly —
  "this is a strong submission for a stretch; the gap is real and the honest framing is
  X" — rather than reporting a bare "failed review".
- `poorly_built` — a judge rejected over something fixable that tailoring should have
  caught. A tailoring miss to own and, budget permitting, fix.

## Hand the artifacts over

Follow SKILL.md "Client deliverables": write `report.md` (read
`references/report-writing.md` first), render and review it, run
`lint_no_prediction.py` (a metric quoted verbatim from the candidate's master, whose
`master-fingerprint.json` still matches, is allowed; never delete a true number to pass
it), then `python3 scripts/deliver.py --workspace <ws>` last (client files go to `~/Downloads/<workspace-name>/`). The
CV goes to `简历/`, the interview brief to `面试准备/`, the report to `报告/`. A cover
letter is provided on demand; it is not the domestic default. Do not start a mock
interview or another mode automatically.

`deliver.py` never converts `cv.md` or `letter.md` to PDF. It copies the `cv.pdf` /
`letter.pdf` that `render_cv.py` / `render_letter.py` or the Word export produced;
when one is missing it delivers the Markdown/Word files, reports `NOTICE_PDF_MISSING`
and exits 2. Produce the PDF and deliver again, or use `--no-pdf` only when the
client asked for no PDF.

CV typography: English uses Times New Roman and Chinese uses SimSun (宋体),
including names and headings, unless the user explicitly requests otherwise. Verify
embedded PDF fonts, not only DOCX settings. Preserve template font sizes and aim for a
well-filled page; never invent content or shrink fonts just to fill a page. The default
Word layout, fictional bilingual examples and native Word/LibreOffice export dialogs are
in `references/word-resume-layout.md`.

When Word files are delivered, `check_pages.py` needs LibreOffice to measure them. A
`DOCX_NOT_MEASURED` finding means Word pagination was not verified: install it and
rerun, or report that limitation. A passing LaTeX PDF does not establish Word pagination.

