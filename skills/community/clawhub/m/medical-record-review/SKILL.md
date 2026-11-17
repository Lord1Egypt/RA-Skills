---
name: medical-record-review
description: >
  Review personal or family health records (lab results, imaging, prescriptions, medication, symptom notes): compare every metric across the full history, draw time trends, report and track data conflicts, grade evidence, and highlight clinical risks.
  Generic layer — it contains no patient data. The project layer injects the profile and all paths.
  Triggers: health record, medical record, lab result, bloodtest, imaging, prescription, medication, symptom, trend, review, analysis, intake, index, registry, merge, rename, audit, 健康档案, 化验, 处方, 用药, 趋势, 复阅, 分析, 建档, 整理, 合并, 更名, 审计, 注册表.
  Never diagnose, never prescribe, never edit source data.
metadata:
  version: "1.5.3"
  language: en
  created: "2026-10-21"
  updated: "2026-10-27"
  source-article: "https://github.com/j3ffyang/ai-thoughts/blob/main/docs/261021-medical-record-review.md"
  changelog: "1.5.3 — add the companion-article alignment appendix and precision notes; correct 'no paths' to 'no patient paths'; record the hand-maintained index contract and non-metric series schema in 1.3.0. 1.5.2 — align the evidence-grading consequence with the article: a failed test drops to `low-confidence`. 1.5.1 — narrow the cross-person comparison claim from 'clinically meaningless' to 'out of scope for this procedure'. 1.5.0 — ship a patient-free AUTHORITY starter at references/AGENTS.example.md, and require a dedicated record folder. 1.4.2 — separate verbatim values from de-identification in §2. 1.4.1 — link the companion article. 1.4.0 — ASD-STE100 pass: one action per sentence, condition first, no semicolons, one name per item. 1.3.0 — four-phase map, fast path, provenance stamp, derived-value rule, hand-maintained index contract, non-metric series schema. 1.2.0 — AI+medical disclaimer. 1.1.0 — English body."
  disclaimer: "Practice of AI + medical combination, not a medical device. Output is not official medical advice, diagnosis, prescription, or treatment decision. No warranty; the author assumes no responsibility for consequences of use or misuse."
---

# Medical Record Review — Generic Health-Record Review

> **This is the generic layer.** It carries no patient data, no patient paths, and no patient values. The project layer injects the profile and the directory layout (see §0).
> **Authority chain**: project `AGENTS.md` > project-layer skill > this generic skill. If they conflict, the higher layer wins. Name the conflicting clause.
> **One record folder = one person.** Multiple people means multiple folders. Folders never reference each other.
> **Terms.** A **record** is one file in `DOCS_DIR`. The **person** is the subject of the record. The **user** is the operator of this skill. Use these three names only.

**Companion article**: [Health Records an Agent Can Audit](https://github.com/j3ffyang/ai-thoughts/blob/main/docs/261021-medical-record-review.md) — why the layers split, and what the skill cannot do yet.

---

> ## ⚠️ DISCLAIMER — AI × MEDICAL IS A PRACTICE, NOT A MEDICAL DEVICE
>
> **This skill is an experiment.** It combines AI with personal medical record keeping. It is an engineering exercise in structure, traceability, and evidence discipline. It is **not** a medical device. No regulator has validated, certified, or reviewed it.
>
> **Its output is NOT an official medical suggestion, recommendation, diagnosis, prescription, or treatment decision.** No licensed clinician writes or reviews this output. Every value, trend, correlation, risk flag, and citation is a machine draft. That draft may be **confidently wrong**.
>
> **Do not act on the output without a clinician.** Never change medication, insulin doses, diet, or treatment on the strength of this output alone. Bring the output to a qualified professional. That professional knows the full history and makes the decision.
>
> **Use at your own risk. The author gives no warranty and accepts no liability.** The skill ships "as is". The author accepts no responsibility for any consequence of use or misuse. Consequences include wrong or harmful action, missed or delayed action, misread data, and data loss. They also include privacy or regulatory harm from the user's own deployment. Sending records to a hosted model, a third-party service, or a shared device is such a deployment.
>
> **The user carries the responsibilities.** The user chooses the model and its egress. The user stores and shares the records. The user protects the identifiers. The user complies with local health-data law. If you cannot accept these terms, do not use this skill.

## Map — four phases, and what may never be skipped

| Phase | Sections | Purpose |
|---|---|---|
| **Ingest** | §0–§2 | resolve configuration, clear egress, file the raw source |
| **Analyse** | §3–§6 | profile, registry, full history, enabled modules |
| **Output** | §7–§10 | conflicts and gates, evidence, risk lanes, output skeleton |
| **Maintain** | §11–§15 | housekeeping, structure, compression, TCM sub-flow, checklist |

A thirty-second answer may drop the optional work. It may never drop the safety rails.

| May skip on a quick answer | Never skipped, at any speed |
|---|---|
| ASCII mini-trends · re-reading the entire registry · optional modules | Egress pre-check (§1) · conflict protocol and change gate (§7) · evidence grading (§8) · one folder per person · never editing a data row |

## 0. Before you start: resolve the configuration

Read the nine keys that the project layer supplies. If a required key is missing, ask the user. Never guess.

| Key | Meaning | If missing |
|---|---|---|
| `AUTHORITY` | Highest rules file, usually the project `AGENTS.md` | Stop and ask |
| `PROFILE` | Where the profile comes from: `AGENTS.md`, `profile.md`, or the user's dictation | Stop and ask |
| `DOCS_DIR` | Record directory (default `docs/`) | Use the default |
| `IMGS_DIR` | Raw scan directory (default `imgs/`) | Use the default |
| `REGISTRY` | Trend-registry filename | Create it on first run, per §4 |
| `INDEX` / `INDEX_CMD` | Index file and its generator command | Maintain by hand. Mark the index as hand-maintained |
| `LANG` | Writing language, and whether existing records are bilingual | Follow the target record's existing language |
| `MODULES` | Enabled analysis modules (see §6) | Enable `western` only |
| `UNWRAP_CMD` | Optional prose-rewrap command | Skip it. Never block on it |

- The project-layer skill holds the configuration. A section of `AGENTS.md` or a standalone `profile.md` may hold it instead. `PROFILE` names the source.
- `AUTHORITY` may point at any rules file the agent already loads. A patient-free starter ships in `references/AGENTS.example.md`. Copy it to the project root as `AGENTS.md`, or point `AUTHORITY` at the host's existing file (`AGENTS.md`, `CLAUDE.md`, or equivalent). The starter carries placeholders only, never a value.
- A record folder is dedicated. Never point `DOCS_DIR` at a mixed folder; §3 reads every record in it.
- **Completeness check**: the project-layer configuration ends with a checklist. A reference template ships one. If the checklist fails, stop. Do not read a record.
- Read profile values fresh every time: age, sex, diagnosis, weight, regimen. Cite the source record. Never fill a gap from memory.

## 1. Egress pre-check (every session, before reading anything)

1. Establish whether the session model is local or hosted.
2. A hosted model means egress. Every record you read enters that provider's context. You cannot recall it.
3. If the task needs zero egress, stop. Switch to a local model. Or have the user dictate the key values.
4. Do not send images, scans, or PDFs to an external vision model without explicit per-file approval.
5. Before you ask, state three things. Say which files would leave the machine. Say what they likely contain. Say where identifiers sit.
6. Use this order: local OCR first, user dictation second, vision delegation last. Before you delegate, strip EXIF and XMP metadata locally. Send a copy only. Keep the original byte-identical.
7. The privacy and egress sections of `AUTHORITY` govern the details. This skill does not restate them.
8. **Originals are top evidence.** Never delete a scan in `IMGS_DIR`. Never overwrite one. Never convert one in place. You can regenerate a derived file. You cannot regenerate an original.

## 2. Intake (file first, analyse second)

- When a new lab result, image, prescription, or symptom note arrives, file it first. Analyse it second. Filing is a write, so get consent first.
- Transcribe into `{{DOCS_DIR}}/{{YYMMDD}}-{{topic}}.md`. Keep every transcribed value verbatim. Do not interpret it. Do not correct it.
- Record arithmetic gaps, illegible readings, and suspect units as found. Then enter them in the pending-decision table (§7) for the user to confirm.
- New records carry YAML frontmatter. The contract is in Appendix B. Do not backfill existing records.
- If `INDEX_CMD` is configured, refresh the index after filing.
- De-identify the transcription. Remove names, institution names, and ID or sample numbers from it. Keep clinically meaningful structure. Write "another institution (different from the previous round)" as the model. The fact that the provider changed survives. The name does not. The original scan in `IMGS_DIR` stays untouched (§1).
- Every new datum must trace to a source. Record the file, the page, the round, the transcription method, and whether a human checked it.
- **Treat the person's own recollection as data.** Label it `patient report, undated` or `patient report, 2026-10`. A document that disagrees with it is a conflict (§7). A remembered dose is not a weaker number. It is a number from a different source.

## 3. Baseline profile (every session)

- Read the index first, if it exists. Then read every record in filename order. Then list `IMGS_DIR`.
- Narrow before you read. Use frontmatter `date`, `type`, and `tags` to shortlist. Then read the full text. **The index is a locator, not a data source.** Every fact still comes from the record.
- Extract what the enabled modules need. Start with an identity-free baseline. Add diagnosis and duration, current medication and doses, diet and exercise, weight history, lab history, and symptom history.
- Cite a source record for every profile line.

## 4. Trend registry (cumulative history)

- If `REGISTRY` is absent, create it. Date it by its first creation day. If it exists, read it and reuse it.
- The date in the registry filename is the creation date. It is not the latest update.
- The registry is a cumulative analysis, not a snapshot. Read it as full history. Never treat it as stale because the filename date is old.
- **Duty one**: normalise each metric across records. Cover name, unit, and reference range. Collapse different abbreviations of one metric here.
- **Duty two**: keep one timeline per metric: `date | value | reference range | status | source record | note`.
- Some metrics depend on measurement conditions: weight, blood pressure, glucose. Carry the condition in the note. State nude or clothed, time of day, fasting or postprandial, and whether the same scale was used.
- Append only. **Never edit a historical data row.** A wrong row goes through the conflict protocol (§7).
- Keep a **pending-decision table** inside the registry. Enter every reported conflict there. Clear nothing until the user decides.
- **Give non-metric series their own minimal columns.** Keep them as separate sections in the registry. Never merge them into the metric table. Define the columns before the first row.
  - Symptoms: `onset | end | severity | attribution status (baseline / after drug X) | source`
  - Formulas: `formula | herb count | per-dose grams | doses | course | relation to previous formula | source`
  - Imaging: `modality | date | finding | positive? | follow-up | source`
  - Any other series: write the column definition next to the table. The next reader then inherits the schema instead of guessing it.

## 5. Full-history comparison

- Never read the latest record alone. Compare against every historical value of that metric.
- Output the trend block as a Markdown table. Cover all metrics in the registry.
- Draw ASCII mini-trends only for high-dimensional metrics with time-series value. Scale them to the historical range (Appendix A).
- Reference ranges differ across institutions and platforms. Never subtract across institutions. Never merge them into one trend. Place them side by side and label the source.
- **Derived values carry their arithmetic.** A derived value is any calculated number: eGFR, a ratio, an index, a unit conversion. Show the formula, the inputs, and the unit. If one of the three is missing, mark the value `low-confidence`. Never present a derived value as a measurement.

## 6. Analysis modules (enabled by `MODULES`)

- **`western` (default on)**: glucose, HbA1c, lipids, liver and kidney function, weight trend, regimen plausibility. Regimen plausibility covers basal-to-bolus ratio, dawn phenomenon, post-meal peaks, and hypoglycaemia protection.
- **`tcm` (optional)**: pattern differentiation, formula decomposition, dose check, warming-cooling balance, decoction and dosing method, course length, dietary restrictions. Sub-flow in §14.
- **`imaging` (optional)**: structured transcription of imaging and functional tests, positive findings, follow-up prompts. Never mix modalities.
- **`cgm` (optional)**: time in range, time above and below range, mean glucose, estimated HbA1c, intraday curve. State the wear period and the coverage.
- **`meds` (optional)**: dosing times, dose-change history, interactions, adherence.
- **Attribution gate (before any causal claim)**: build the medication timeline first. Record the start date, the stop date, the gap between regimens, and any other drug taken in between. Then decide whether the symptom predates the drug (baseline) or follows it. Never attribute a symptom change to a drug or formula before this step.
- **Applicability check**: before you cite an external conclusion, verify that it holds for the current profile. Check age, sex, ancestry, diagnosis subtype, duration, complications, weight, and current medication. A general-population range is not this record's target. If the conclusion does not hold, mark the claim `low-confidence`.

## 7. Conflict protocol (hard) and the data-change gate

Triggers for a conflict:

- The same metric differs across records.
- Definitions or conditions do not match.
- The arithmetic does not reconcile.
- One event has two versions.
- The person's recollection contradicts a document.

Procedure:

1. Stop.
2. Name the records, the locations, and every version of the value.
3. Classify the cause. Choose one: transcription slip, changed definition, different measurement condition, or a genuinely new value.
4. Hand the conflict to the user. Edit only after the decision.

Log every reported conflict in the pending table. After the decision, mark it resolved and record the decided value. **Never delete an undecided conflict.**

Never do these three things. Never pick one value silently. Never "fix" the original silently. Never write an uncertain value into a trend as fact.

**Change gate** — every data edit passes it, not only conflicts:

1. Re-read the original source and compare.
2. List the change as "old value → new value + basis".
3. Edit only after the user confirms.

**Scope of an exemption**: a user exemption covers process notes and analysis lines only. The user may allow a rewrite or a deletion there. **Data rows are never editable.** Data rows are values, source columns, reference ranges, and measurement-condition flags. You can append a data row or resolve it. You cannot rewrite it.

- **Pure appends** skip the comparison above. A pure append is a new row or a new section. A pure append still needs permission to write that record. A pure append must carry its source.

## 8. Evidence grading (output discipline)

Every external claim passes five tests. If a claim fails one test, it drops to `low-confidence`.

1. **Safety** — an uncertain detail means stop and verify. Never trade correctness for speed.
2. **Factuality** — the source exists and says what you claim. Never invent studies, guidelines, or numbers.
3. **Verifiability** — another agent can find and read the same source. Give the citation trio: source name, year or guideline edition, and PMID or URL. A Wikipedia mention is not a source.
4. **Specificity** — the source applies to the current profile (see the applicability check in §6).
5. **Credibility** — the provenance is independent. Flag industry funding, conflicted authors, or advocacy origin.

- A missing element of the citation trio demotes the claim to `low-confidence`. A demoted claim goes to "clinician review".
- **Never infer a missing detail to complete a claim. Name what is missing.** Name the missing evidence, the missing local reference range, or the missing current state.
- **Write the two kinds of statement apart.** A record fact is sourced and re-checkable. An external inference needs evidence. The first is a record. The second is a judgement. Never put both in one sentence.

## 9. Risk highlighting

Always emit a risk block with three lanes:

- **Actionable**: clear evidence and a defined target.
- **Monitor**: evidence is insufficient now. Add the item to the next review.
- **Clinician review**: the claim fails the five tests in §8, or it lies outside this skill's boundary. Diagnosis and prescribing lie outside that boundary.

- Every risk carries its evidence source. Analysis is informational. It never replaces medical advice.
- **Never claim a review that did not happen.** Do not label output "verified", "approved", "clinically validated", or "confirmed by a clinician". Use such a label only after a named clinician read that output. Automation is not review.

## 10. Output skeleton (fixed order)

A full review follows this order. A quick answer may compress to ②④⑤.

| # | Block | Content |
|---|---|---|
| ① | Baseline profile | one source per line |
| ② | Metric trends | new value against full history, plus ASCII |
| ③ | Arithmetic check | totals, products, units, date consistency |
| ④ | Conflicts | new reports, pending-table sync |
| ⑤ | Analysis | in `MODULES` order. Each module splits into record facts and external inference |
| ⑥ | Risks | actionable / monitor / clinician review, each with evidence |
| ⑦ | Housekeeping | stale marks, heading levels, naming, index refresh result |

## 11. Housekeeping

- Before you append, re-read the analysis lines this skill produced earlier. If a record update made one stale, mark it "superseded" or revise it in place. This applies to analysis lines only. Never apply it to data rows.
- Recheck every number in play: totals, products, unit conversions, and date-to-round matching.
- Confirm that the pending table is in sync. Enter new conflicts. Resolve decided ones.
- Append with `##` and `###` only. Never add a second `#`. Keep one H1 per record.
- Name each record `YYMMDD-topic`. The topic must match the content. It answers one question: what data would I open this for.
- **Never cite a line number.** Cite the section heading plus the item name. Line numbers drift.
- **Markup checks are heuristics.** They need human judgement. Never use them as a pass/fail gate.
  - Unbalanced bold: `awk 'gsub(/\*\*/,"")%2==1 {print FILENAME": "FNR}' <file>`. Horizontal rules of `***` are false positives. Inspect the suspect lines only.
  - Label missing its colon inside a list: `grep -nP '^([0-9]+\.|- )\*\*[^：]+?\*\*(?!：)' <file>`. This check covers Chinese punctuation only. Compare within one list level. Lookaround needs `grep -P`. Built-in grep and ripgrep lack it.
- **Appending a log entry is error-prone.** Use these guard rails.
  1. `oldString` must contain the previous entry in full. `newString` keeps that entry verbatim and appends the new one.
  2. The common failure: `oldString` holds part of the previous entry, and `newString` holds only the new one. The previous entry is then destroyed.
  3. Verify at once with `grep -c` that every entry appears exactly once.
- **Rendering escapes**: write `<3` as `\<3`. Write a standalone `$` as `\$`. Otherwise the renderer eats them.
- **Stamp what wrote an analysis.** End every analysis block with a provenance line: `provenance: <model> · <date> · <skill version>`. Models change. Without the stamp, nobody can re-judge a five-year-old paragraph.

## 12. Document structure · merge and rename

Classify the record before you write.

| Class | Rule |
|---|---|
| **Event record** | One record per episode. The filename date is the event date. A follow-up joins its own episode record |
| **Series record** | Multiple rounds from one source. Append, never fork. The filename carries the latest data round's date. The header states "rename and re-point references when a new round lands" |
| **Analysis record** | Derived from other records. Mark it "inference / review". It produces no raw data. The filename date is the creation date |
| **Historical archive** | No follow-up value. Excluded from metric tables. Kept as-is |

- **One record, one meaning.** Each lab round or prescription episode gets its own record. Cross-round summaries live only in the registry. Those summaries are definitions, trends, and charts. Do not backfill a merged record.
- Never let a filename collide with a later record's date.
- **Merge procedure.** Fidelity comes from construction, not from review.
  1. Concatenate byte-for-byte with `sed` ranges or a raw copy. Never retype. Never rewrite.
  2. Order the sections by content date.
  3. Name the record after the episode's anchor date. Do not use the newest content date.
  4. Re-point every reference, including source columns.
  5. **Keep old filenames verbatim inside update logs.** They are change traces, not typos.
  6. Write a merge note at the end. Include the original name, its own merge history, "content unchanged", and whether the file was renamed.
  7. Delete the old record.
  8. Self-check four things. Exactly one H1. Bold is balanced. Escapes are handled. No stale reference survives outside the historical logs.
- **Rename procedure**:
  1. Settle the semantics from the table above.
  2. Re-point every reference, source columns and relative links included.
  3. Record old → new, the reason, and the reference count.
  4. **No bulk replace.** Edit reference by reference. Then run `grep` on the historical log lines to prove they are untouched. A bulk replace once rewrote a history line. That failure is recorded.
- **Check the blast radius first.** Run `grep -rn`, ignored directories included. Confirm that nothing lives outside this repository.

## 13. Auditing and compressing a cumulative record

**Four audit steps**:

1. Quantify per section. Count characters and lines. Never hunt by feel.
2. Find superseded intermediate states. Most "conflicts" in a cumulative record are old states replaced by later entries: pending → decided, missing → complete.
3. Find same-record duplication. One fact restated in prose, a table, and a matrix.
4. Find cross-record second copies. The same content lives in a dedicated record.

**Two preconditions**:

1. Get an explicit user exemption from the rewrite restriction. Record it in the file as a format-change line with the date and the approval. The exemption scope is in §7.
2. Do not touch data rows.

**Execution: candidate → machine check → swap.** This path covers compression, excision, and merge.

1. Build the candidate in `/tmp`.
2. Verify three counts. Expected-deletion markers must be 0. Expected-kept markers must be at least 1. The data-row diff must contain only intended changes.
3. Swap only after the check passes. On failure, the original stays untouched.

- **Deleting an option that was never executed: keep the class, drop the name.** Remove the specific regimen, brand, or dose. Keep the class-level clinical red line.
- **Deletable**: process notes are deletable, and only on request. Process notes are backfills, re-records, corrections, and rename records.
- **Not deletable**: trust and condition flags. These are unverified, estimated, pending, not-recorded, measurement conditions, and source columns.
- **Cleanup**: delete candidate files and temporary extracts as soon as the swap succeeds. Leave no cache behind.

## 14. TCM prescription sub-flow (when `MODULES` includes `tcm`)

**0. Collect this field set before analysis.** Never guess a missing field. Mark it "not recorded (pending)".

- Practitioner, surname only.
- Institution, de-identified.
- Patient statistics.
- Pattern differentiation. Mark each item as the practitioner's words or the person's report.
- Symptoms and the four examinations. Mark missing items "not recorded".
- Herb table.
- Formula elements: herb count, per-dose total, number of doses, grand total, decoction method, administration, and dietary restrictions. "None" is also a finding. Add any patent medicine and its composition, the course length, and the relation to the previous formula.
- Follow-up.

Then run six checks:

1. Check the herb count and the doses. Sum each herb to get per-dose grams. Multiply doses by per-dose grams to get the grand total. Match the herb count to the table rows.
2. Decompose into functional groups. Check each herb's role and dose.
3. Assess the warming-cooling balance. Compare the cold herbs with the warming counter-agents.
4. Check contraindications and interactions. Cover the classic incompatibilities, laxative herbs against loose stools, and stacking with current Western drugs.
5. **Review toxicity.** A herb is risky when it is aconite, Aconitum, Aristolochia, raw Pinellia, raw Arisaema, over-dose Asarum, or Tripterygium. Mark a risky herb name in **bold** with a ⚠️.
6. State that herb's toxicity and monitoring points in the risk block.

## 15. Completion checklist

- [ ] Nine config keys resolved. Missing ones confirmed with the user
- [ ] Every profile line cites a source. Nothing filled from memory
- [ ] New values compared against full history. No cross-institution subtraction
- [ ] All numbers rechecked: totals, products, units, dates
- [ ] Conflicts all reported. The pending table is in sync
- [ ] External claims pass §8. The citation trio is complete
- [ ] Record facts and external inference written apart
- [ ] Risks sorted actionable / monitor / clinician review, each with evidence
- [ ] Registry appended. Historical data rows untouched
- [ ] Index refreshed, if a generator is configured
- [ ] Naming, heading levels, escapes, and source labels consistent
- [ ] Derived values show formula, inputs, and unit
- [ ] Analysis blocks carry a provenance stamp: model, date, skill version
- [ ] `IMGS_DIR` originals untouched. Nothing deleted or overwritten in place
- [ ] No output claims clinician verification that did not happen
- [ ] No identifiers leaked. No unapproved push or transfer

## Appendix A · ASCII mini-trends

One block per metric: a Markdown timeline table and a mini-trend. Scale the trend to the historical range, oldest to newest.

```
<metric> (<unit>) — <period old→new>
<high mark> |            ● ← <date> <note>
<mid mark>  |     ●
<low mark>  |  ●
            +------------------------→ time (old→new)
```

## Appendix B · Frontmatter and index contract

```yaml
---
date: YYYY-MM-DD        # event record = event date; series = latest data round; analysis = creation date
type: event | series | analysis | archive
topic: short-slug       # must answer "what data would I open this for"
source: where the data came from (file / round / transcription method)
status: trust flag (official / estimated / model-transcribed, unchecked ...)
tags: [keyword, keyword]
---
```

- **Frontmatter is the single source of truth for machine fields.** The blockquote header stays human prose. It explains why the record exists, its limits, its de-identification, and its rollback path. It does not restate the machine fields. Frontmatter wins a conflict.
- The index is **generated**. Hand edits are overwritten on the next run, and they become a second copy of the truth. Change content in frontmatter. Change structure in the generator.
- **If no generator exists**, the index is maintained by hand. Its first line must read `hand-maintained: true`. Readers then treat it as a hint, not as a machine-truth source. They re-verify every field against the record it points to.
- Do not backfill existing records that lack frontmatter. The index shows them as `no-frontmatter`.

## Appendix C · Precedent library (lives in the project layer)

This skill deliberately embeds no precedents. Precedents belong to specific records and specific institutions. The project layer keeps a table with at least three columns: precedent, ruling, and origin. The precedent is what happened. The ruling is what to do next time. The origin is the record and the date.

- Precedents state the structural lesson only. Never copy values. Cite the record when a number matters.
- Reference a precedent by section heading. Never by line number.
- Before you add a precedent, check for an existing rule. If a rule covers it, fold the precedent into that rule and attach "reason: precedent X". Never state the same rule twice.

## Appendix D · Boundaries, disclaimer, sharing

- **Read the highlighted disclaimer at the top of this file first.** It is the operative statement. It says this is a practice of AI + medical combination, not a medical device. It is not official medical advice. It offers no warranty. The author assumes no liability for use or misuse. The user carries deployment and legal responsibility. Everything below is a consequence, not a replacement.
- This skill does not diagnose. It does not assign a disease subtype. It does not prescribe. It does not adjust doses. It does not replace a clinic visit.
- Output is informational. Any change to medication or treatment belongs to a clinician.
- Egress responsibility sits with the user. A hosted model means egress, and egress cannot be recalled. Before you share a record folder, settle who may read it and where it may travel.
- One folder per person. The project layer injects configuration and profile per folder. **Never reference across folders.** Cross-person comparison is out of scope for this procedure, and it leaks.
- Record version changes in the frontmatter `version` field and in the project layer's change log. A structural change also updates the completion checklist.

## Appendix E · Locale profiles

The workflow is language-neutral. Set `LANG` in the project layer, then apply the conventions below.

| Concern | Chinese (zh) | English (en) |
|---|---|---|
| Paragraph wrapping | One paragraph per line, never hard-wrapped mid-sentence | Same |
| Joining rewrapped prose | No space between CJK characters, a single space otherwise | Single space |
| Punctuation | Full-width `，。：；「」` inside prose. The colon check in §11 targets `**label：**` | ASCII punctuation. The `grep -P` colon heuristic does not apply |
| Headings and tables | Chinese accepted inside headings and cells | English throughout |
| Bilingual records | Append in the record's existing language. A new standalone record may be monolingual | Same |
| Transliteration | Pinyin only for rare or easily misread characters | None |
| Quote marks | 「…」 in Chinese prose. Do not mix with `"…"` in one record | `"…"` or `'…'`, consistently |
| Escapes | `<3` → `\<3`. Standalone `$` → `\$` | Same |
| Traditional / Simplified | State which variant the record uses. Convert with a deterministic tool, never by hand | Not applicable |

- Mixed-language records are allowed only when the project layer says so. Otherwise pick one language per record.
- The escape rules apply in every locale. Markdown renderers interpret the characters, not the language.

## Appendix F · Companion article alignment (precision notes)

> **This appendix aligns vocabulary. It does not add authority.** The companion article [Health Records an Agent Can Audit](https://github.com/j3ffyang/ai-thoughts/blob/main/docs/261021-medical-record-review.md) is a reference. It explains why the procedure exists and what it cannot do. This skill is the procedure. Where the article's shorthand and this skill differ, this skill wins. Nothing in either document is a medical device, official medical advice, a diagnosis, a prescription, or a treatment decision. The user carries the risk. If either document and a clinician disagree, the clinician wins.

**Term map.** The article names the rules informally. Use these sections.

| Article term | Where this skill defines it |
|---|---|
| Append-only data rows | §4 |
| Conflict protocol | §7 |
| Change gate | §7 |
| Exemption scope | §7 |
| Evidence five | §8 |
| Applicability | §6 (applicability check) |
| Attribution timeline | §6 (attribution gate) |
| Single copy | §13 steps 3–4; Appendix B |
| Derived-value arithmetic | §5 |
| Provenance stamp | §11 |

**Shorthands that need a precise reading.**

- **"Conflict gate"** in the article means the conflict protocol **and** the change gate. Both are never skipped. They are separate steps in §7.
- **"No paths"** in the article means no **patient** paths. This skill uses `{{DOCS_DIR}}` path templates and default `docs/` and `imgs/` folders. It carries no patient paths and no patient values.
- **"The template carries rules and configuration"** means it does not carry the profile values. The profile lives in the file `PROFILE` names. `AGENTS.example.md` also carries a profile section, boundaries, and the completeness check; those are instructions, not patient data.
- **"The starter"** is `references/AGENTS.example.md`. It is a template, not an active authority file. Copy it, or point `AUTHORITY` at an existing rules file.
- **"Project layer"** is the project-layer skill, or the `AGENTS.md` section that `AUTHORITY` names. The nine keys live in one place, not both.
- **"Clinical judgement"** in the article means the clinician's judgement. This skill structures evidence and flags risks. It does not own clinical authority. The clinician's judgement wins.
- **"Actionable"** in the risk block means actionable **by a clinician**. This skill does not authorize a dose change, a treatment change, or a self-treatment decision.

**Precision notes.**

1. **A pure append is still a write.** It skips the old→new comparison. It still needs permission to write the record, and it must carry its source. §7.
2. **The change gate applies to changes to existing data rows.** Pure appends are handled by note 1. §7.
3. **A hand-maintained index is a hint, not machine truth.** Its first line must read `hand-maintained: true`. Readers re-verify every field against the record. Appendix B.
4. **A failed evidence test drops the claim to `low-confidence`.** A missing element of the citation trio also demotes it to `low-confidence`. A demoted claim goes to clinician review. §8.
5. **The output skeleton does not repeat the disclaimer.** The disclaimer sits at the top of this skill. A generated review can omit it. The companion article flags this as a strain. §10.
6. **The template's rule sections are five, not four.** Privacy, egress, evidence, measurement conditions, and data changes. `AGENTS.example.md` §2–§6.
7. **The index contract and the non-metric schema came from the same review as the provenance stamp and the derived-value rule.** See the 1.3.0 changelog entry. This is why the article says "four gaps."
