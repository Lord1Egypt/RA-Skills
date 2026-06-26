---
name: medication-side-effect-visit-log
displayName: "Medication Side Effect Visit Log"
version: "1.0.0"
description: "Create a clinician-ready timeline and visit brief for possible side effects after a medication or supplement start, stop, or change."
triggerKeywords: [medication side effect log, side effect tracker, medication symptoms, side effects after new medicine, doctor visit side effect notes, pharmacist questions, medication change symptoms]
tags: [health-literacy, medication-safety, side-effects, patient-advocacy, visit-prep, symptom-log]
license: "MIT-0"
language: "en"
hasExecutableCode: false
---

# Medication Side Effect Visit Log

## Safety Boundary

This skill is a communication and tracking aid for possible medication or supplement side effects. It does not diagnose, determine causality, recommend dose changes, suggest starting or stopping medication, rank medication risks, or replace a clinician, pharmacist, poison control center, or emergency care.

Do not tell the user to start, stop, skip, split, combine, substitute, ration, or change any medication. Do not infer whether a symptom is caused by a medication. Keep language neutral: "happened after" or "the user noticed" rather than "caused by."

Ask only for information the user is comfortable sharing. Do not request full prescription numbers, insurance IDs, national IDs, payment details, account passwords, portal credentials, or private medical records.

If the user reports severe allergic reaction, trouble breathing, chest pain, fainting, severe swelling, suicidal thoughts, overdose, confusion, seizure, severe rash, or any emergency symptom, tell them to seek emergency care or contact local emergency services immediately.

## When to Use

Use this skill when the user wants to:

- Prepare notes for a doctor, pharmacist, nurse, or clinic after a medication or supplement change.
- Track symptoms that started, stopped, worsened, or improved after a medication start, stop, dose change, timing change, refill, brand/generic switch, or supplement change.
- Build a neutral timeline from medication changes to symptom patterns.
- Separate observed facts from worries, guesses, or internet research.
- Create questions to ask a clinician or pharmacist.

Do not use this skill to:

- Decide whether a medication is safe for the user.
- Decide whether symptoms are side effects.
- Provide medical advice, diagnosis, treatment, dosing, tapering, or medication substitution.
- Replace urgent care for severe or rapidly worsening symptoms.
- Interpret lab results, drug interactions, pregnancy risk, or complex medical conditions.

## Intake Questions

Ask only the minimum needed to build the log:

- What medication, supplement, or change are you concerned about? Use the name only if that is enough.
- What changed: started, stopped, dose changed, timing changed, missed dose, refill changed, brand/generic changed, or supplement added?
- When did the change happen? Approximate date and time are fine.
- What symptoms or changes did you notice?
- When did each symptom start, how often does it happen, how long does it last, and how severe is it on a 0-10 scale?
- What else changed around the same time: sleep, meals, alcohol, caffeine, exercise, illness, stress, travel, menstrual cycle, other medicines, supplements, missed doses, or new routines?
- Who do you plan to contact: prescribing clinician, pharmacist, primary care clinician, specialist, nurse line, urgent care, or another professional?

If the user volunteers dose schedule, record it exactly as user-stated. Do not ask follow-up dosing questions unless needed to summarize what the user already provided.

## Response Workflow

Follow this sequence:

1. Start with the safety boundary and urgent-care reminder if any serious symptoms appear.
2. Capture the medication or supplement change in user-provided terms.
3. Record symptoms neutrally with onset, duration, frequency, severity, and trend.
4. Add context factors that may help a clinician interpret the timeline.
5. Build a chronological timeline from change to symptoms and follow-up actions.
6. Separate observed facts from user guesses, fears, assumptions, and questions.
7. Generate concise questions for the clinician or pharmacist.
8. Produce a visit brief and ongoing tracking table.
9. End with a next-contact checklist, not medical advice.

## Medication Change Snapshot

Create this section first:

| Item | User-provided details |
|---|---|
| Medication or supplement name | [name or placeholder] |
| Change type | Started / stopped / changed dose / changed timing / missed dose / refill or brand change / supplement added / other |
| Date and time of change | [date/time or approximate] |
| User-stated schedule, if volunteered | [copy exactly or write "not provided"] |
| Prescriber or source, if relevant | [clinician / pharmacist / over-the-counter / supplement / not provided] |
| Planned contact | [doctor / pharmacist / clinic / nurse line / urgent care / other] |

Keep this factual. Do not add interpretation.

## Symptom Pattern Table

Use a table like this:

| Symptom or change | First noticed | Duration | Frequency | Severity 0-10 | Trend | Notes for clinician |
|---|---:|---:|---:|---:|---|---|
| [neutral description] | [date/time] | [minutes/hours/days] | [once/daily/etc.] | [0-10] | Better / worse / same / comes and goes | [facts only] |

Guidance:

- Use the user's own words when possible.
- Avoid diagnostic labels unless the user says a clinician already used them.
- Convert vague timing into approximate ranges without inventing precision.
- Mark missing details as "unknown" instead of guessing.

## Context Factors

Ask about and summarize only relevant context:

| Factor | Notes |
|---|---|
| Sleep | [changes, missed sleep, usual pattern] |
| Meals and hydration | [with food, skipped meals, dehydration concerns] |
| Alcohol, caffeine, nicotine, or cannabis | [if user volunteers or relevant] |
| Exercise or exertion | [new or unusual activity] |
| Stress, anxiety, or major life event | [if user wants to include] |
| Illness or infection | [cold, fever, stomach illness, etc.] |
| Other medication or supplement changes | [names only if user provides them] |
| Missed doses or timing changes | [user-stated facts only] |
| Travel, altitude, heat, or schedule change | [if relevant] |

Do not imply these factors explain the symptoms. Present them as context for the professional.

## Timeline Builder

Create a chronological timeline:

| Date/time | Event | Source | Notes |
|---|---|---|---|
| [date/time] | Medication or supplement change | User report | [exact user wording] |
| [date/time] | Symptom first noticed | User report | [duration/severity if known] |
| [date/time] | Contacted pharmacy/clinic | User report | [what they said, if provided] |
| [date/time] | Current status | User report | [better/worse/same] |

If events are uncertain, label them "approximate." Do not infer missing cause-and-effect.

## Facts vs Questions

Separate the brief into three lists:

### Observed Facts

- [Medication or supplement change, date/time]
- [Symptom pattern, date/time]
- [Context factors]
- [Professional contacts already made]

### User Concerns or Guesses

- [Concern in user wording]
- [Internet research or fear, clearly labeled as unverified]

### Questions to Ask

- Could these symptoms be related to the medication or something else?
- What symptoms should make me seek urgent care?
- Should I continue taking the medication exactly as prescribed while waiting for guidance?
- Are there timing, food, alcohol, caffeine, or interaction issues I should understand?
- Should I track anything specific before the next appointment?
- Who should I contact if the symptoms worsen after hours?

Adapt questions to the user's situation without answering them yourself.

## Visit Brief Output

Produce a concise brief the user can paste into a portal message or bring to a visit:

```text
Medication Side Effect Visit Brief

Reason for contact:
I noticed [symptoms] after [user-described medication/supplement change] on or around [date]. I am not changing how I take it without professional guidance and would like advice.

Medication/supplement change:
- Name: [name]
- Change: [started/stopped/changed/etc.]
- Date/time: [date/time]
- User-stated schedule, if volunteered: [schedule or not provided]

Symptoms:
- [symptom]: started [date/time], lasts [duration], occurs [frequency], severity [0-10], trend [trend]
- [symptom]: ...

Context:
- [sleep/meals/caffeine/alcohol/exercise/stress/illness/other changes]

Questions:
1. [question]
2. [question]
3. [question]

Urgent symptoms:
Please tell me what symptoms would require urgent care or emergency services.
```

## Ongoing Tracking Table

Offer this table for the user to continue tracking:

| Date/time | Medication taken as prescribed? | Symptom | Severity 0-10 | Duration | Context notes | Action taken | Follow-up needed |
|---|---|---|---:|---|---|---|---|
| YYYY-MM-DD HH:MM | Yes / No / not applicable / prefer not to say |  |  |  |  |  |  |

Do not use this table to advise changes. It is for communication with a professional.

## Red Flag Reminder Language

Include this reminder when appropriate:

"If you have trouble breathing, chest pain, severe swelling, fainting, seizure, severe rash, confusion, suicidal thoughts, overdose concern, or symptoms that feel urgent or rapidly worsening, seek emergency care or contact local emergency services now. This log is not a substitute for urgent medical help."

## Example Prompts

Copy and paste one of these into your AI assistant with your details filled in:

1. **New medication, new symptoms:** "I started lisinopril 10mg three days ago and have been feeling dizzy in the mornings and having a dry cough at night. I take it at 8 AM with breakfast. No other medications changed. I have a follow-up with my doctor next Tuesday. Help me build a timeline and visit brief to bring to the appointment."

2. **Dose change concerns:** "My doctor increased my sertraline from 50mg to 100mg last Monday. Since then I've had trouble sleeping, some nausea around midday, and feel more anxious than usual. I also started a new multivitamin last week. My psychiatrist appointment is in 5 days. Create a side-effect log with timeline and questions."

3. **Multiple medication changes:** "I started a new blood pressure medication two weeks ago and stopped a different one at the same time. I've noticed fatigue in the afternoons and occasional headaches. I also changed my diet around the same time. I need to discuss this with my pharmacist before my next refill. Help me organize what to ask."

## Output Format

Return the result in this order:

1. Safety note and urgent-care reminder.
2. Medication change snapshot.
3. Symptom pattern table.
4. Context factors.
5. Timeline.
6. Facts vs concerns vs questions.
7. Clinician or pharmacist visit brief.
8. Ongoing tracking table.
9. Next-contact checklist.

Keep the tone calm, neutral, and practical. The artifact should help the user communicate clearly without making medical claims.
