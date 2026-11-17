# Workflow checks

Read only the checks for the selected mode and artifacts. Narrow text edits do not enter this workflow.

## Hand-off — offer the next mode, never run it

A mode ends where a person has to choose. `modes/discover.md` says it "never
chains into `apply` — thirty rows do not become thirty CVs", and that rule holds
in every direction, not just that one.

**Offering is not chaining.** The difference is whether a person chose. A model
that reads "never chains" as "never mentions" leaves the user at the end of a
mode with no idea the other three exist — which is not restraint, it is the
skill hiding itself. So when a mode completes, say what it produced and then ask
which of these they want next, in one question with selectable options:

| finished | offer next | why |
|---|---|---|
| `discover` | `assess` a row that interests them | the full-posting read and discovery mapping can be extended into the selected role's complete assessment |
| `assess` | `apply` if the verdict is worth it | and say the verdict out loud first — `blocked` gets one honest ask, not a silent refusal |
| `apply` | `interview` on the package just built | the CV now makes specific claims; the mock round is where the candidate finds out whether they can defend them |
| `interview` | `apply` again to fix what the round exposed | an undefendable claim is a CV bug, not a story to drill |

Two rules on the offer itself:

- **Never run one unasked**, including when the answer looks obvious. The user
  who wanted only a CV should get a CV and a question, not four modes of work.
- **Do not offer a mode whose inputs are not there.** `interview` needs a built
  application or a posting plus CV for an upcoming interview; `assess` needs a posting. Offering a mode that would immediately
  ask for something the user does not have wastes the question.

**No gate prints this offer, deliberately.** `modes/apply.md` Step 7.6 carries it,
because a gate's stdout is one finding per line with a stable CODE prefix — an
always-on line there trains the reader to skip the channel that reports real
findings, and a gate that says what to do next is prompting rather than checking.
The hand-off is the mode file's job, and `test_mode_declaration_and_handoff.py`
holds both halves: that apply mode ends by offering the next modes, and that
`check_apply` stays silent on stdout when it is clean.

**A passing gate does say one thing, on stderr.** `journal.receipt()` prints
`PASS: <gate> — no findings. This is not the end of the <mode> run; return to
modes/<mode>.md …` whenever it writes a `pass` verdict. That is not the offer
above and not a next command: it names no successor, because which step follows
belongs to the mode file and a per-gate list here would go stale the first time
a step moved. It exists because total silence was measured to be worse than the
noise. On 2026-10-08 two agents walked discover and apply using only what the
files and scripts print, and both stopped at the first green light and called
the round finished — the four discover completion gates exit 0 with zero bytes
of stdout between them, with `report.md`, the coverage check, the render and
the delivery all still to do. stdout keeps its contract; stderr is where this
repo already puts `NOTICE_*`.

## Gates

| Gate | Script | Fires on |
|---|---|---|
| Personal data | `scripts/check_personal_data.py` | protected fields on a Cluster-1 target, or an unrecognised market. The renderer WITHHOLDS them for both — an unrecognised market is the conservative default, not a pass — and says so on stderr; markets are matched by ISO code, English name, endonym (`Nederland`, `España`, `한국`, `Việt Nam`) and CJK name |
| Rendering refusals | `scripts/render_cv.py` | right-to-left text (Arabic, Hebrew, Syriac, Thaana, N'Ko): the LaTeX template has no `bidi`, so a PDF would come out reversed and unshaped at exit 0. The PDF and the `.tex` are both refused as `UNSUPPORTED_SCRIPT` — a **tolerated** failure, so Markdown and .docx still ship and the exit code is unchanged. Paper is `letterpaper` for a US/CA target and `a4paper` otherwise; `meta.paper` overrides for the other Letter-using countries |
| Claim provenance | `scripts/check_claims.py` | a term with no source (skills, certifications, titles, orgs, degrees, institutions, project roles, publications, awards, volunteer, board); a status qualifier dropped off a real credential — in every language this skill writes CVs in, so `(in Bearbeitung)`, `(nog niet afgerond)`, `（修了見込み）`, `(재학중)` and `（在读）` count exactly as `(in progress)` and `B1` do; a publication status dropped off a paper (`(under review)`, `(submitted)`, `preprint`, `manuscript in preparation`, `unpublished`, 投稿中/审稿中/在审, 査読中, 심사 중), including `under review at <venue>` dropped with its venue (`in press` and `accepted` are not in the list: dropping them claims nothing); a subordinate-rank qualifier dropped off a title (Assistant/Associate/Junior/Deputy/Vice/Acting/Interim/Trainee/Intern, 副/助理/实习, 補佐/見習い, 부/수습 …; dropping Senior/Lead is a de-escalation and stays quiet); an employer or institution name shortened beyond its legal form, group designator or comma-delimited sub-unit (`ORG_TRUNCATED`); a title, degree or project role taken from a different master entry, matched by dates and employer (`TITLE_FROM_OTHER_ENTRY`; quiet when the dates say two entries were merged onto one line); a mutated master profile |
| Verdict parsing | `scripts/parse_verdicts.py` | anything that is not exactly PASS/REJECT; a non-unanimous round |
| Render freshness | `scripts/check_render_freshness.py` | a judge that read a file the disk no longer has |
| CV lint | `scripts/lint_cv.py` | clichés, weak openers, over-long bullets, repeated verbs; the 2026 AI vocabulary from `scripts/prose_tells.py` (`AI_VOCABULARY`). The cliché and vocabulary scans run over the WHOLE document, not only the bullets — the summary is the line a recruiter reads first, and it used to be the one line nothing checked. Headings and the contact line are skipped, so an employer called "Robust Systems" is not reported as a cliché. A CV is exempt from the structural checks: a skills line reads "Python, C++, MATLAB" and would fire the tricolon check on every correct CV. Skills, certifications and publications, and the `**title**, employer` entry header, are names rather than phrasing and are not scanned for `AI_VOCABULARY`; a publication is exempt from every wording rule. Japanese and Korean bullets are verb-final and are not counted for `REPEATED_VERB` |
| Letter | `scripts/check_letter.py` | machine-prose tells over the whole body — the 2026 AI vocabulary (`AI_VOCABULARY`), em-dash density (`EM_DASH_DENSITY`), the "not just X, but Y" pivot (`NOT_JUST_PIVOT`) and tricolon density (`TRICOLON_DENSITY`), all from `scripts/prose_tells.py`, whose thresholds are calibrated against real letters including this skill's own; markdown in a body string, length, duplicated name, wrong company/role; a missing salutation or sign-off in a language this skill has no sourced default for (`NO_SALUTATION` / `NO_CLOSING`) — the renderer no longer prints an English one onto a non-English letter, so the gate is what stops it shipping with none. The 250–350 band is an ENGLISH word count, so a CJK-dominant letter is reported (`NOTICE_CJK_LENGTH_UNSCORED`, stderr) rather than scored — this skill has no sourced length convention for one, and the one-page constraint behind the band is measured directly by `check_pages` on the rendered PDF Its receipt also hashes `tailored-profile.yaml` (and `profile.yaml` when the first has no `meta`) whenever the letter's language comes from the profile, so a profile edit makes `check_apply` report `STALE_RECEIPT`; re-run `check_letter`. In `EM_DASH_DENSITY`, `——` counts as one mark and Han/kana are measured one character per unit |
| Page count and PDF text | `scripts/check_pages.py` | a PDF longer than the market's table allows; a letter over one page; an unreadable PDF; a PDF whose text is missing `meta.name` or an `experience[].org`, or whose text cannot be read at all (`UNVERIFIED_PDF_TEXT` — not a pass); a start date in a calendar it cannot read (`START_DATE_UNREAD` — years of experience is then *unknown*, not zero, and the permissive budget is used rather than the strictest; not reported when `meta.max_pages` or an academic `cv_type` sets the budget, since the date then decides nothing) |
| Template layout review | `scripts/check_layout.py` | missing/stale requirements, reference or final-file fingerprints; measured font, size, color, paper or margin mismatches; a PDF replaced after Word export; uninspected pages or unresolved differences. `--report` reviews the report separately and requires the current `report.md` prose, in order and as whole lines, in `report.pdf`, with table cells present (`REPORT_PDF_TEXT_MISMATCH`). Measurements supplement the eight actual visual comparisons; failures require repair and re-review. See `references/layout-review.md`. |
| Word limits | `scripts/check_word_limits.py` | a supporting-statement criterion over its stated limit, empty, or with no limit recorded; and the machine-prose tells from `scripts/prose_tells.py`, measured per criterion so the finding names which answer to rewrite. This is the artifact that is actually MARKED — the three CV judges are routed away from a structured application by design — and it had no reader for its prose at all. Limits are read whole: `1,000`, `1.000`, `1 000`, `1'000`, `250-word`, `1,000字以内`, `1,000자 이내` |
| Apply completion | `scripts/check_apply.py` | a missing receipt; a receipt that does not match its own `receipt_hash`, i.e. hand-written or edited rather than produced by a gate (`RECEIPT_UNVERIFIED`); a gate that only ran its `--record` setup (`NOT_VERIFIED`); ANY gate left failing, named or not; an unclassified stop; a missing brief. `RECEIPT_UNVERIFIED` and `MODE_FILE_MISSING` are checked by every composer — apply, assess, discover and interview — not just this one |
| Mock interview | `scripts/check_mock.py` | an invented tag or band; a tag with no quote, or a quote that is not in the transcript; a pass emitting the other pass's tags; a scraped question with no id, no date, or the wrong country; an answer-bank entry with no source; a collapsed claim with no walk-back; an unsourced fact neither promoted nor walked back |
| Evidence blocks | `scripts/evidence_blocks.py` | the posting and CV cut into addressable `JD-nnn` / `CV-nnn`; the only chunker |
| Evidence refs | `scripts/check_evidence_refs.py` | refs that resolve to no block; block ids left in reader-facing prose |
| Prediction lint | `scripts/lint_no_prediction.py` | percentages (incl. fullwidth `％` and 「百分之七十」), `n/m` scores, scores worn as a NOUN rather than a symbol (`匹配度 85 分`, `overall score: 85`, `rated 8.5`, `4.5 stars`, `confidence: 0.85`, `grade: B+`, `Bewertung 8`, `점수 85점`), and prediction vocabulary in every language it writes in — EN + ZH (「成功率」「入围率」「七成」…) plus DE/NL/FR/ES/IT/JA/KO (`Chancen`, `kans`, `probabilité`, `可能性が高い`, `확률`) in the **judgement-facing** artifacts: `fit-assessment.md`, `shortlist.md`, `cheatsheet.md`, `mock/answer-guide.md`, `mock/assessment-*.md`. Numbers the round actually CAPTURED are exempt, but only from a file an `adapter_call` record names or an intact `browser_call` snapshot — a raw file nobody journaled is not a capture, it is a note the model wrote itself. Deliberately NOT the CV or letter — there a number is a measured past achievement, which the Quantification ladder above requires, not a claim about the future Also numberless certainty bound to an outcome (肯定能拿到面试, 进面稳了, `definitely get an interview`, `almost guaranteed`, `Sie bekommen sicher ein Interview`, `vous aurez certainement un entretien`; en/zh/ja/ko/es/de/nl/fr/it), also across one short means/time phrase or comma aside (肯定能通过内推拿到面试, `You will definitely, with this CV, get an interview`). Allowed: likelihood whose object is a question or topic (会被问到, 八成会问到, 聞かれる可能性が高い, 질문받을 가능성이 높다, `es probable que te pregunten`, `likely to be asked`, `ti chiederanno sicuramente del progetto`, `vragen ze zeker naar je scriptie`, `werden Sie wahrscheinlich nach Ihrem Projekt gefragt`, `on vous demandera probablement votre motivation`; unless the same sentence first receives an outcome: 面接に呼ばれて…聞かれる可能性が高い still fires, a conditional 面接に進んだら… does not), a negated certainty (没人能肯定你会拿到面试, `no one can say for certain that you will get an interview`), discipline names (概率论, `probability theory`, `maximum likelihood`), dates with a four-digit year and `24/7`, and a metric quoted with its neighbouring words from a trusted source: `posting-source.txt`, the CV bound by `evidence-blocks.json` (hash must match; never a file under scan or one the run writes: `report.md`, `cv.md`, anything under `mock/`, `judge-*`, any `.md/.pdf/.docx/.html/.yaml/.json` in the workspace outside `inputs/` and `source/`; `cv-source.txt` is the default), or the master bound by `master-fingerprint.json` (hash must match, master outside the workspace). Scans `report.md` as well |
| Contradictions | `scripts/consistency.py` | verdict vs effort, loose knockouts, gaps with no action, work-authorization conflicts — reports, never repairs |
| Coverage counts | `scripts/count_coverage.py` | the only count-producing path **wherever a `fit-assessment.yaml` exists** — assess mode, and apply mode resumed from one. Apply mode without an assessment has no file for it to read and hand-counts its FIT SNAPSHOT instead; that is a second path, so it must apply the identical rule (below), and it is why the rule is written out in both places rather than trusted to memory. The card renders in **zh, en, ja, ko or es** using the same counts; pair it with the required text in [report-localization.md](report-localization.md). Other languages embed an English or Chinese card and required labels. Missing judgements, evidence and disclaimers remain failures in every supported language |
| Market tables | `scripts/check_conventions.py` | digits/percent in prose, source provenance, protected traits, duplicate ids, expired `review_by` (CI-hard) |
| Assess | `scripts/check_assessment.py` | composes the six above and requires their receipts; disclaimer, disqualifier section, the “What to do instead” half, verbatim conventions, stale-review banner; a top-level `level_direction` or `effort` the card prints but nobody assessed, and a work-authorization token spelled outside its set |
| Migration losslessness (CI only) | `scripts/check_skill_lossless.py` | a baseline line that exists nowhere in this tree |
| Hidden characters (CI only) | `scripts/check_hidden_chars.py` | a soft hyphen, zero-width character, BiDi embedding/override/isolate or tag character anywhere in source or docs — a line that reads one way to a person and another to the interpreter. No allowlist; the fix is an escape or removal. Exits 2 on an empty tree, because 0 findings over 0 files is not a clean scan |
| Adapter classification | `scripts/check_opencli_result.py` | *(wrapper, not a gate)* a non-zero exit, a login wall, a platform stop-signal, or an empty identity field. It exits **1 whenever the classification is not `ok`** and prints `ADAPTER_READ_NOT_OK` on stderr, so a caller that branches on `$?` cannot read a failed fetch as a success; the classification stays on stdout for a caller that parses it |
| First-run environment | `scripts/doctor.py` | *(precondition, not a gate)* every capability the skill needs, checked by USING it — the PDF check renders a PDF, because an earlier `command -v xelatex` check called a working machine broken while tectonic was installed. `--install` installs the Python packages; the agent prepares required tools and daily-browser CDP via `references/agent-setup.md` |
| Saving a master | `scripts/save_profile.py` | *(guarded write, not a gate)* one master per language; a new language never overwrites another, a repeat language is backed up first, and a profile with no `meta.language` is refused |
| Delivery | `scripts/deliver.py` | *(hand-off, not a gate)* requires a client `report.md` and verified report PDF; puts requested client documents together in `~/Downloads/<workspace-name>/` (or shared `--to` folder) and prints the path. Exits 0 or 2, never 1. `DELIVER_DEST_UNWRITABLE` is macOS TCC refusing `~/Downloads` mid-session — say so and offer `--to`, never leave the artifacts undelivered |
| Read-only | `scripts/check_no_write.py` | a journaled command whose published `access:` is `write`, or whose access cannot be resolved at all |
| Discovery profile snapshot | `scripts/snapshot_profile.py` | *(guarded helper, not a gate)* freezes `candidate-profile.yaml` for one search round and refuses to replace it with a changed master, so later CV edits cannot silently rewrite matching evidence |
| Candidate match | `scripts/check_candidate_match.py` | a high verdict or default recommendation that lacks a complete row-specific detail, a frozen-profile evidence pointer, a valid requirement mapping, or its localized reader-facing summary; a card promoted without detail; a core gap hidden by optional preferences; a stale ordering or more detail mappings than `brief.max_match_reviews` permits; `detail_unmapped` verifies a full read without counting as a CV mapping |
| Weekly digest | `scripts/check_digest.py` | an email that was not composed from the current picks; more than five roles; a role not in the shortlist, not read in full, without a link, reason or gaps, or already sent; a source that was not checked but is not named; prediction language; the round's own `check_shortlist` failing. `digest.py sent` runs it and records nothing on findings |
| Shortlist | `scripts/check_shortlist.py` | a row whose `source_id` or `raw_text` is in no raw capture, whose `id` is not `<site>-<source_id>`, or whose direct posting URL is empty, malformed, or not returned by its source; a candidate missing that clickable URL in `shortlist.md`; a duplicated or over-counted source report; "no results" with no adapter that exited 0; a missing disclosure block or the wrong provisional stamp for card-only versus detail-reviewed output; a detail fetch outside the top three; an uncapped brief, or a run that exceeded the caps the brief declares; a posting URL rendered in `shortlist.md` that is in no `shortlist.yaml` row; a row whose company or salary contradicts its own capture; a missing or stale mode entry. Warns (does not fail) when a row's location names a country outside `brief.markets` |

**No mode may claim success while `journal.jsonl` lacks a receipt for its gates.** A skipped script produces no output, and no output is exactly what a clean run looks like. `scripts/check_skill_lossless.py` is the one exception and is marked as such: it is a repo-level CI check with no workspace and no receipt, so requiring one would be requiring evidence that cannot exist.

<!-- BEGIN discover-inserts (plan 3) -->

## Self-check — run through this before reporting the package as done

- [ ] Drafting or revising a client report? Read `references/report-writing.md`,
      complete the separate full-report reader review: read every section/table,
      assess reasonableness, logic and readability, fix and reread the entire
      revision, then read the final PDF. Record concrete findings privately;
      preserve every posting's city/link and inspect navigation and typography.
      For each summary/table pair, reconcile category names, level and order,
      and map each direction to visible company-and-title rows; do not pass an
      unexplained mismatch merely because the text and layout checks pass.
- [ ] Domestic job discovery? Reconcile the WeChat source plan with captured
      queries, original articles and recruitment conditions; identify unread or
      inaccessible leads. A successful search command is not completed research.
- [ ] Following a report example? Compare its applicable tables, columns,
      numbered jobs, field labels, preparation lists and directory with both the
      final Markdown and PDF. Recheck every explicit user correction; do not
      accept a font/color match while the information structure is missing.
- [ ] Client delivery? Read the entire report without the private test notes:
      it must give career decisions and actions, with no fixture or test-process
      narration. For a requested full-page CV, check the final Word-export PDF's
      page count, measured content bottom and natural spacing before delivery.

- [ ] On a site refusal, follow `references/user-recovery.md`: explain the reason,
      preserve partial results, wait for explicit user confirmation before a new
      linked round; do not clear the stopped journal.

- [ ] Daily-browser CDP and parallel sources: follow `references/daily-browser.md`;
      verify the selected profile, isolate tabs and share site budgets.
- [ ] Browser capture: read `references/browser-fallback.md` and record each
      actual snapshot with `scripts/record_browser_capture.py` before another read.
      Use `browser_page` evidence and stop across tools after a site refusal.
      Navigation requires a journal-derived budget and a catalog selector for
      every stage; final-page rows alone cannot establish round compliance.

Read-when:
- [ ] Reviewing a Word or PDF CV? Follow `references/layout-review.md` and compare every rendered page with the supplied template and the user's later changes.
- [ ] Page unavailable? Follow `references/network-recovery.md`: classify first,
      use bounded retries, and inspect relevant VPN/split-routing evidence.
- [ ] Diagnosed OpenCLI adapter incompatibility? Read `references/opencli-compat.md`;
      `scripts/opencli_compat.py` checks optional, reversible local patches.
      Browser fallback does not require patching; a site refusal still stops reads.
- [ ] Running on a host that is not Claude Code — codex, another agent, or as a
      subagent without `AskUserQuestion`? Read `references/portability.md`.
- [ ] Not a software/research/engineering role? Read `references/role-families.md`.
- [ ] Employment gap >6 months, career switch, re-entry, over/under-levelled, thin
      experience, executive, military transition or international credentials?
      Read `references/candidate-situations.md`.
- [ ] Essential/Desirable criteria, behaviours or a scored supporting statement?
      Read `references/structured-applications.md` — it REPLACES the CV judge loop.
- [ ] Writing a letter? Read `references/motivation-letter.md` (skip gate first).
- [ ] Japan + traditional/domestic employer? Read `references/rirekisho.md`.
- [ ] Building or reordering the CV? `references/cv-craft.md`.
- [ ] Rendering a Word CV? Follow `references/word-resume-layout.md` and inspect the exported pages.
- [ ] Doing gap analysis or tailoring? `references/gap-analysis.md`.
- [ ] Extracting a posting? `references/job-posting-extraction.md`.
- [ ] Writing the brief? `references/interview-prep.md`.
- [ ] In apply mode? `modes/apply.md`, loaded on entry, not on demand.
- [ ] In interview mode? `modes/interview.md`, loaded on entry, not on demand — and
      `references/interview-shapes.md` in full before the first question.
- [ ] In discover mode? `modes/discover.md`, loaded on entry, not on demand.
- [ ] A discover gate reported a finding? Read `references/discover/finding-codes.md`.
- [ ] Writing a report that compares several postings? Also read `references/discover/multi-posting-report.md`.
- [ ] Matching a discovered role to a CV? Read `references/candidate-matching.md`,
      then run `scripts/snapshot_profile.py` once to freeze
      `candidate-profile.yaml` before mapping any detail.
- [ ] About to make the first live retrieval of a run, or asked to page further,
      fetch more detail pages, or work while the user is away?
      `references/source-policy.md`.
- [ ] About to call a discovery adapter? Read its current metadata in
      `references/discovery-sources.md`.
- [ ] An adapter call exited non-zero? `references/risk-control-signals.yaml`
      carries the stop-signal patterns `scripts/check_opencli_result.py` matches.

Dispatched:
- [ ] `agents/ats-screener.md`, `agents/recruiter-screener.md` and
      `agents/hiring-manager.md` were each pasted IN FULL into their own judge.
- [ ] `agents/mock-assessor-transcript.md` and `agents/mock-assessor-provenance.md` were
      each pasted IN FULL into their own assessor, with **different** input packs.

Ran, with a receipt in `journal.jsonl` — `scripts/check_apply.py` requires each of these
unconditionally:
- [ ] `scripts/check_personal_data.py`
- [ ] `scripts/check_claims.py` — the VERIFYING run. The `--record` run at mode entry
      fingerprints the master and checks nothing; its receipt says `baseline_recorded`
      and `check_apply` reports it as `NOT_VERIFIED`, not as a pass.
- [ ] `scripts/check_render_freshness.py` — recorded before dispatch AND verified after.
      Same rule: the dispatch record is `baseline_recorded`, the verifying run is the
      one that counts, and re-recording for the next round does not carry the last one.
- [ ] `scripts/parse_verdicts.py` — its receipt reports on the PARSE. A cleanly parsed
      round is `recorded` whatever the three judges said; `fail` means a judge returned
      no usable `VERDICT:` line and must be re-dispatched.
- [ ] `scripts/lint_cv.py`

Required too, but only when the artifact they read is on disk — `check_apply` keys each
one on the file, so "it did not apply" is never guesswork:
- [ ] `scripts/check_letter.py` (when `letter.yaml` exists)
- [ ] `scripts/check_layout.py` (when `cv.docx` or `cv.pdf` exists; inspect all pages against the supplied template first)
- [ ] `scripts/check_pages.py` (when `cv.pdf` AND `tailored-profile.yaml` exist — both
      are its inputs, and a `could_not_run` receipt does not satisfy it)
- [ ] `scripts/check_word_limits.py` (when `supporting-statement.md` exists, or
      `posting.yaml` says `application_type: structured` and the statement is missing)

Ran, with a receipt — but `scripts/check_apply.py` does NOT require these, so skipping
one is silent and only this line reports it:
- [ ] `scripts/check_apply.py` — the composer itself; it cannot require its own receipt.
- [ ] `scripts/check_mock.py` (once per mock-interview round — interview mode, not apply)

`check_apply` also fails on ANY gate in this workspace's journal whose latest receipt
says `fail`, named on the lists above or not — a receipt from another mode excepted.
Enumerating gates does not keep up with the gates: `check_pages` and `check_word_limits`
were both off the required list, so either could run, print `CV_TOO_LONG` / `OVER_LIMIT`,
and have `check_apply` write its own `pass` three lines below it in the same file.

Ran, leaving a `mode_entry` record rather than a gate receipt:
- [ ] `scripts/enter_mode.py` — and its recorded hash still matches `modes/apply.md`.

Ran, leaving nothing in the journal (they render; they do not judge):
- [ ] `scripts/render_cv.py`, plus `scripts/render_letter.py` /
      `scripts/render_rirekisho.py` if applicable.
- [ ] `scripts/deliver.py` — the LAST step of every mode. A workspace under
      `~/.claude/job-profiles/` is where the skill works, not where a person
      looks, and a path pasted into a chat message is gone once it scrolls.
- [ ] `references/supplementary-sources.md` — career source selection, WeChat articles and source quality.
- [ ] `scripts/pdf_glyphs.py` — shared painted-glyph validation used by page checks and delivery.
- [ ] `scripts/layout_requirements.py` — imported measurement checks used by `check_layout.py`; verify reference-derived requirements for CV and report.
- [ ] `scripts/doctor.py` — once per machine, before the first mode. Reports
      capabilities by using them; `--install` covers the Python packages only. Follow
      `references/agent-setup.md` to install required tools and prepare daily-browser CDP.
- [ ] `scripts/setup_dependencies.py` — prepare the private runtime when required;
      `scripts/run_tool.py` invokes it without depending on global executables.
- [ ] `scripts/browser_cdp.mjs` — diagnosed fallback reads only; import the capture
      through `scripts/record_browser_capture.py` before the next same-site read.
- [ ] `scripts/save_profile.py` — every master save goes through it. One CV per
      language, and a new language never overwrites another's file.

In CI, not in a workspace (no receipt exists for these, by design):
- [ ] `scripts/check_skill_lossless.py` — only when this skill's own files changed.
- [ ] `scripts/check_hidden_chars.py` — whenever any source or documentation file
      changed. The source repository runs it in `make check` and in CI; wherever it is
      run, a literal invisible character is replaced by an escape or removed, never
      waived.

Ran, with a receipt in `journal.jsonl` — the discover gates. `scripts/check_apply.py`
does not require these; a discover run is not reportable without them:
- [ ] `scripts/check_no_write.py` (discover)
- [ ] `scripts/check_candidate_match.py` (discover; after the profile snapshot and before the shortlist)
- [ ] `scripts/check_shortlist.py` (discover); final `scripts/deliver.py` must check
      complete descriptions for all retained postings across collection rounds,
      or captured access failures with visible reasons. Cards are allowed in an
      explicitly requested preliminary report, not a completed consultation.
- [ ] `scripts/check_search_coverage.py` (complete discover/collection delivery):
      register planned sources and directions before retrieval; close every
      planned pair and observed lead with evidence. Round limits, target counts
      and `shortfall` do not mean completion. Delivery rechecks current evidence.
      See `references/search-coverage.md` for the multi-round manifest and schema.

Ran, leaving an `adapter_call` record rather than a gate receipt:
- [ ] Every adapter invocation classified exactly once — by `run_tool.py --workspace`
      for its own reads, or by `scripts/check_opencli_result.py` for another runner's
      capture. It is a wrapper, not a gate: it exits 1 when the classification is not
      `ok` and 2 when it could not classify, and leaves an `adapter_call` record rather
      than a receipt. Classifying the same read twice records two calls.

Every line above says what evidence it leaves, and the headings differ for a
reason: a checklist that promises a receipt where none can exist teaches its reader
that one of its lines is decorative, and the reader cannot tell which one.

In assess mode:
- [ ] Assessing a posting? `modes/assess.md`, entered with `scripts/enter_mode.py`.
- [ ] Writing a Japanese, Korean or Spanish discover/assess report?
      `references/report-localization.md` for native headings, counts and disclosures.
- [ ] Rendering a market convention card? `references/market-conventions/README.md` is the
      rule for what may be in one; the tables are `references/market-conventions/cn.yaml`,
      `references/market-conventions/nl.yaml`, `references/market-conventions/de.yaml`,
      `references/market-conventions/uk.yaml`, `references/market-conventions/us.yaml`.
- [ ] Printed the cards with `scripts/convention_cards.py --market <market> --lang <lang>`
      instead of reading the table, and copied its text and any stale banner verbatim?
- [ ] Ran `scripts/evidence_blocks.py`, `scripts/count_coverage.py`,
      `scripts/consistency.py`, `scripts/check_evidence_refs.py`,
      `scripts/lint_no_prediction.py` and `scripts/check_assessment.py`, and quoted
      `check_assessment`'s receipt? `scripts/check_conventions.py` runs in CI over all five
      tables.

Told the user:
- [ ] All three verdicts and the ATS coverage line, verbatim, each round.
- [ ] The internal FIT SNAPSHOT and its required disclaimer, before and after; client advice is written separately.
- [ ] Which market and language the CV was calibrated for.
- [ ] Any remaining honest gaps, and — if the loop ended un-passed — whether this is
      POORLY BUILT or an HONEST STRETCH.
- [ ] The consultation folder and its client report/CV files; keep internal files private.
- [ ] **The delivered files** `deliver.py` printed — in one `~/Downloads/<workspace-name>/` folder, including the report PDF.
      That is the one the user can actually open; the workspace path is for an audit.
- [ ] In discover: before delivering a complete report, read the full description
      of every retained posting. Search-card summaries serve internal triage and
      do not satisfy this requirement. If access genuinely fails, retain a failure
      capture, explain the reason in the report and mark the posting unresolved;
      never count it as detail-reviewed. Show the Sources and read quality table,
      the trigger reason and each posting's actual read status. Full detail review
      is still distinct from a complete application assessment; use the matching
      disclosure from `modes/discover.md` and `references/report-localization.md`.
      **Write the output in the user's language.** Keep one language per document.

CV typography: English uses Times New Roman and Chinese uses SimSun (宋体),
including names and headings, unless the user explicitly requests otherwise.
For reports, follow `references/word-resume-layout.md`: an explicitly selected
font/template wins; otherwise the portable renderer may use its embedded fonts.
Verify embedded PDF fonts, not only DOCX settings. Preserve template font sizes
and aim for a well-filled page; any added gap before a section heading is at
most one blank line. Never invent content or shrink fonts just to fill a page.

- [ ] Rendering a report? Run `scripts/render_report.py`, then the page review and report layout gate in `references/layout-review.md`.
- [ ] Use `scripts/layout_pages.py` for canonical previews and verified unchanged-page reuse. Inspect all pending pages; run the normal layout gate afterward.
- [ ] Delivering a report? Check the candidate/target/date/mode filename generated by `scripts/report_names.py`; preserve user-edited or unrecorded old reports.
- [ ] Weekly job email (setup, change, stop or a scheduled run)? Follow `references/weekly-digest.md`: `scripts/digest.py` for every step, and `scripts/check_digest.py` must pass before anything is sent.
- [ ] Entering apply, discover or assess? Follow `references/online-presence.md`: run `scripts/online_presence.py status` first, ask once for any profile it lists under `to_ask`, never re-ask a recorded answer, and write back only confirmed findings.
- [ ] No report template? Write the report's layout requirements with `scripts/report_requirements.py` once `report.md` exists, before rendering.
- [ ] Need this resource index? Read only the relevant checks in `references/workflow-checklist.md`.
