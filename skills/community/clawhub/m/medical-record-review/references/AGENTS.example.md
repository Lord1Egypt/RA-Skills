# AGENTS.md — Health Record Project Rules (AUTHORITY)

> **Copy this file to your record project root as `AGENTS.md`.** It is the `AUTHORITY` file that `medical-record-review` reads before it touches a record. It contains no patient data, no paths, and no values.
> Fill every `<...>` placeholder. If a required key is unresolved, the skill stops and asks. Do not default.
> `AUTHORITY` does not have to be named `AGENTS.md`. Point it at the rules file your agent already loads (`AGENTS.md`, `CLAUDE.md`, or equivalent).

## 1. Scope

- One record folder holds one person. Folders never reference each other.
- This folder holds health records and their configuration only. Never point `DOCS_DIR` at a folder that also holds code, other projects, or unrelated notes.
- This file governs privacy, egress, evidence, and data changes. The procedure lives in the generic skill.
- This file outranks the project-layer skill. The project-layer skill outranks the generic skill. Name the conflicting clause when they disagree.

## 2. Privacy red lines (non-negotiable)

- Never write a name, an institution name, an ID number, a sample number, a phone number, an address, or a date of birth into a record.
- Keep the record folder local. Do not sync it to a cloud drive, a shared folder, or a team drive.
- Never compare two people clinically. Never copy a value from one person's folder into another's.
- Keep every original scan byte-identical. Never delete, overwrite, or convert an original in place.
- De-identify a transcription. Write "another institution (different from the previous round)" as the model. The fact that the provider changed survives. The name does not.

## 3. Data egress (decide before you read)

- Decide whether the session model is local or hosted before you open a record.
- A hosted model means egress. Every record read enters that provider's context, and you cannot recall it.
- If the task needs zero egress, use a local model, or have the user dictate the key values.
- Do not send an image, scan, or PDF to an external vision model without per-file approval.
- Use this order: local OCR first, user dictation second, vision delegation last.
- Strip EXIF and XMP locally before delegation. Send a copy only.
- State three things before you ask for approval: which files leave the machine, what they likely contain, and where the identifiers sit.

## 4. Evidence standard

- Separate a record fact from an external inference. Never write both in one sentence.
- Give every external claim the citation trio: source name, year or guideline edition, and PMID or URL.
- A missing element of the citation trio drops the claim to `low-confidence`.
- Never invent a study, a guideline, a number, or a citation. Name what is missing instead.
- Check applicability before you cite an external conclusion: age, sex, ancestry, diagnosis subtype, duration, complications, weight, and current medication.
- A general-population range is not this record's target.

## 5. Measurement conditions

- Carry the condition with the value: nude or clothed, time of day, fasting or postprandial, same scale or a different one.
- Never subtract, or plot on one trend line, values taken under different conditions. Flag the mismatch.

## 6. Data changes

- Data rows are append-only. A wrong row goes through the conflict protocol; it is never edited in place.
- Every data edit passes the change gate: old value → new value + basis, then a human yes.
- A user exemption covers process notes and analysis lines only. It never covers a data row.
- A conflict stops the work. Name both versions, classify the cause, and hand the decision to the user.

## 7. Configuration (the nine keys)

Replace each `<...>` with a real value before the first run.

| Key | Value |
|---|---|
| `AUTHORITY` | this file |
| `PROFILE` | `<profiles/member.md>` |
| `DOCS_DIR` | `<docs/>` |
| `IMGS_DIR` | `<imgs/>` |
| `REGISTRY` | `<docs/YYMMDD-metrics-trend.md>` — create it on the first run |
| `INDEX` / `INDEX_CMD` | `<docs/index.md>` / `<python3 scripts/gen_index.py>` — if there is no generator, maintain the index by hand and mark it `hand-maintained: true` |
| `LANG` | `<en>` or `<zh>` |
| `MODULES` | `<western>` — add `tcm`, `imaging`, `cgm`, or `meds` as needed |
| `UNWRAP_CMD` | `<optional; omit if unset>` |

## 8. Profile

- `PROFILE` names the file that holds age, sex, diagnosis and duration, medication with dosing times, measurement conditions, and the two or three things this person actually cares about.
- Keep the profile free of names. Cite a source record for every value. Read the values fresh every session; never fill a gap from memory.

## 9. Boundaries

- This project does not diagnose, assign a disease subtype, prescribe, or adjust a dose.
- Output is a draft. It is not official medical advice, not a medical device, and not a treatment decision.
- Bring every output to a qualified clinician. That clinician knows the full history and makes the decision.

## 10. Completeness check

Confirm all five before the first run. If one fails, stop and fix it.

- [ ] Every placeholder in this file is filled with a real value
- [ ] `AUTHORITY` points at this file, and no key is left unresolved
- [ ] `PROFILE` exists, cites a source per value, and carries no names
- [ ] The record folder holds one person only, and no folder references another
- [ ] The egress policy matches the model in use for this session