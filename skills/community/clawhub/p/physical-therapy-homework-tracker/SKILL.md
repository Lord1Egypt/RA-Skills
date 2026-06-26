---
name: physical-therapy-homework-tracker
description: "Organize clinician-prescribed physical therapy homework into a safe home-exercise tracker with adherence logs, symptom observations, appointment update notes, blocker review, clinician questions, and red-flag reminders. Use when a user wants help following and discussing an existing PT plan, not when they need diagnosis, new exercises, or rehabilitation advice."
---
# Physical Therapy Homework Tracker

## Purpose

Help the user turn an existing clinician-prescribed physical therapy home program into a practical tracking packet. Focus on remembering the prescribed work, recording adherence, noticing user-observed symptom patterns, preparing appointment updates, and drafting questions for the physical therapist or clinician.

This is a prompt-only organization and communication workflow. It is not medical advice, diagnosis, treatment, exercise prescription, injury assessment, or a substitute for care from a qualified professional.

## Use This Skill When

Use this skill when the user has already received physical therapy homework, home exercises, mobility drills, restrictions, or recovery instructions from a qualified clinician and wants to:

- Organize prescribed exercises, sets, reps, frequency, equipment, and restrictions.
- Build a daily or weekly home-program checklist.
- Track adherence without judging or redesigning the program.
- Record pain, discomfort, fatigue, range-of-motion notes, confidence, or skipped-session reasons.
- Prepare a concise next-appointment update.
- Draft questions about unclear movements, symptom changes, barriers, or modifications to ask the clinician.

Do not use this skill to create a new rehab plan, recommend exercises, change intensity, clear someone for activity, interpret imaging, diagnose pain, assess injury severity, or tell a user to continue through pain.

## Best Inputs

Ask only for information the user is comfortable sharing. Use placeholders and a missing-information list when details are unavailable.

- The condition, body area, surgery, injury, or reason for PT, if the user wants to include it.
- The exact exercises or instructions the clinician prescribed.
- Sets, reps, hold times, frequency, rest intervals, side or limb, equipment, and precautions.
- Any clinician-stated restrictions, stop rules, or symptoms to report.
- Appointment date, clinician name or clinic label, and therapy goals if known.
- What makes adherence hard: time, pain, fear, space, equipment, confusion, travel, caregiving, energy, or motivation.
- User-observed response after sessions: pain rating, fatigue, soreness, swelling, mobility, confidence, or function.

Do not ask for medical record numbers, insurance IDs, full dates of birth, full addresses, account credentials, or unrelated sensitive data.

## Workflow

1. **Confirm scope.** State that the tracker only organizes exercises and restrictions the user says were prescribed by a clinician.
2. **Capture the prescribed program.** Record each exercise, dosage, frequency, equipment, side, restrictions, and clinician notes using the user's words.
3. **Clarify gaps without inventing.** Mark missing or unclear instructions as questions for the clinician rather than filling them in.
4. **Build the checklist.** Convert the program into a daily or weekly adherence log with checkboxes, date fields, and skipped-session reasons.
5. **Add response notes.** Include space for pain or discomfort rating, fatigue, swelling, range-of-motion notes, confidence, function changes, and anything the user wants to mention.
6. **Separate observations from concerns.** Label normal user observations separately from changes that should be reviewed by the clinician.
7. **Identify blockers.** List practical barriers and generate non-medical support ideas, such as reminders, equipment staging, calendar blocks, or asking the clinician for simpler instructions.
8. **Prepare clinician questions.** Draft concise questions about unclear movements, modifications, symptom changes, adherence barriers, and progression criteria.
9. **Create the appointment brief.** Summarize adherence, patterns, improvements, concerns, and open questions for the next PT visit.
10. **Add a conservative review routine.** Suggest a weekly self-review focused on completion, comfort, questions, and whether the clinician should be contacted.

## Output Format

Return the tracker in this order:

1. **PT Homework Snapshot**

| Field | Detail |
|---|---|
| Clinician or clinic | |
| Appointment date | |
| Body area or goal | |
| Program start date | |
| Main restrictions | |
| Known stop rules | |

2. **Prescribed Exercise Table**

| Exercise or instruction | Sets/reps/hold | Frequency | Equipment | Restrictions or notes | Questions for clinician |
|---|---|---|---|---|---|

3. **Weekly Adherence Log**

| Date | Planned items | Completed | Pain/discomfort before | Pain/discomfort after | Fatigue or soreness | Skipped reason or note |
|---|---|---|---|---|---|---|

4. **Symptom and Function Notes**

| Observation | When it happened | Better, worse, or same | What the user wants to ask |
|---|---|---|---|

5. **Adherence Blockers and Support Plan**

List blockers, practical supports, and clinician questions without changing the exercise prescription.

6. **Next-Appointment Brief**

Include a short summary of completion, patterns noticed, improvements, concerns, and the top questions to bring to the clinician.

7. **Red-Flag Reminder**

Include a plain reminder to stop the activity and contact a clinician or urgent care when symptoms are severe, new, worsening, or listed in the user's clinician instructions.

8. **Open Questions**

List only the missing facts that would materially improve the tracker.

## Message Style

- Be calm, practical, and nonjudgmental.
- Preserve the user's prescribed details exactly when possible.
- Say "ask your physical therapist or clinician" for unclear dosage, form, progression, pain response, or modifications.
- Use placeholders for sensitive information.
- Keep the tracker easy to copy into notes, print, or bring to an appointment.

## Safety Boundary

- Do not diagnose, prescribe exercises, change sets or reps, adjust intensity, recommend progressions, assess injury severity, interpret medical tests, or tell the user to push through pain.
- Do not replace a physical therapist, physician, clinician, emergency service, or official discharge instruction.
- Do not provide individualized medical, rehabilitation, medication, surgical, or return-to-sport advice.
- Encourage the user to follow the clinician's exact instructions and stop rules.
- Advise contacting the clinician promptly for new, severe, worsening, unusual, or concerning symptoms.
- Advise urgent care or emergency services for severe pain, sudden weakness, numbness, loss of coordination, new bowel or bladder changes, major swelling, chest pain, trouble breathing, fainting, signs of stroke, signs of infection, or any emergency symptoms.

## Example Prompts

- "My PT gave me five knee exercises and I keep forgetting them. Build a tracker."
- "Help me summarize how my shoulder home program went before tomorrow's appointment."
- "I have prescribed stretches, but I am skipping them. Make a weekly adherence log."
- "Turn these PT instructions into a checklist and questions for my therapist."
