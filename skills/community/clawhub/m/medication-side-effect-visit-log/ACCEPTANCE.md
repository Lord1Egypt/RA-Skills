# Acceptance Criteria Checklist

- [x] Directory is `~/.openclaw/skills/medication-side-effect-visit-log`.
- [x] Contains exactly `SKILL.md`, `skill.json`, and `ACCEPTANCE.md`.
- [x] `SKILL.md` has YAML frontmatter with name, description, version, trigger keywords, tags, license, language, and `hasExecutableCode: false`.
- [x] `skill.json` is valid JSON and includes version `1.0.0`, license `MIT-0`, language `en`, and `hasExecutableCode: false`.
- [x] Skill is prompt-only: no scripts, APIs, network calls, credentials, package files, or executable instructions.
- [x] Trigger is clear: possible medication or supplement side effects after a start, stop, or change.
- [x] Deliverable is concrete: medication change snapshot, symptom pattern table, timeline, questions, visit brief, and ongoing tracker.
- [x] Workflow has 5-10 ordered steps and supports clinician or pharmacist communication.
- [x] Safety boundary is prominent: no diagnosis, causality claim, dose change, medication stop/start advice, or urgent-care replacement.
- [x] Privacy boundary avoids prescription numbers, insurance IDs, national IDs, payment details, passwords, and unnecessary health data.
- [x] Emergency escalation language covers severe allergic reaction, trouble breathing, chest pain, suicidal thoughts, overdose, confusion, seizure, severe rash, and rapidly worsening symptoms.
- [x] Differentiated from `doctor-visit-prep`, `pharmacy-prescription-problem-log`, and `blood-pressure-pattern-journal` by focusing on side-effect pattern capture after medication changes.
- [x] English-only content; no CJK text.

## Install-First Success Path

- **Input:** User says "I started lisinopril 10mg three days ago and have been feeling dizzy in the mornings and having a dry cough at night. I take it at 8 AM with breakfast. No other medications changed. I have a follow-up with my doctor next Tuesday. Help me build a timeline and visit brief."
- **Steps:** Skill states safety boundary and urgent-care reminder (severe allergic reaction, trouble breathing, chest pain, etc.) → captures the medication/supplement change in user-provided terms (name, change type, date/time) → records symptoms neutrally with onset, duration, frequency, severity, and trend → adds context factors (sleep, meals, alcohol, caffeine, exercise, illness, stress) → builds a chronological timeline from change to symptoms and follow-up actions → separates observed facts from user guesses, fears, and assumptions → generates concise questions for the clinician or pharmacist → produces a visit brief and ongoing tracking table → ends with a next-contact checklist.
- **Output:** A medication side effect visit log with medication change snapshot, symptom pattern table, context factors, chronological timeline, facts-vs-concerns separation, clinician/pharmacist questions, visit brief, ongoing tracking table, and next-contact checklist — all communication-focused without diagnosis or medication advice.

## Clean Scan Evidence

- **Executable code:** None (prompt-only, noExec)
- **API calls:** None required
- **Network access:** No (document-only)
- **Credentials:** None stored or requested
- **Secrets or .env:** None
- **Logs or temp files:** None
- **Package files or scripts:** None
- **Safety scan:** Clean — does not diagnose, determine causality, recommend dose changes, or suggest starting/stopping medication; keeps language neutral ("happened after" not "caused by"); does not request prescription numbers, insurance IDs, or private medical records; includes emergency escalation for severe allergic reaction, breathing trouble, chest pain, suicidal thoughts, overdose, seizure, severe rash.
