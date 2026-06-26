---
name: migraine-trigger-pattern-log
description: "Create a clinician-friendly migraine or recurring headache pattern log with episode timelines, possible context factors, symptom notes, medication response tracking, red-flag guidance, and a concise appointment summary. Use when the user wants to observe patterns without self-diagnosing or changing treatment on their own."
---
# Migraine Trigger Pattern Log

## Purpose

Help the user turn recurring migraine or headache episodes into a clear observation log they can use personally or bring to a clinician. The skill produces a lightweight tracking template, a pattern review, and a doctor-visit summary while avoiding diagnosis or treatment advice.

This is a prompt-only health tracking workflow. It is not medical advice and does not replace care from a qualified clinician.

## Use This Skill When

Use this skill when the user reports any of these situations:

- Recurring migraines, headaches, or suspected trigger patterns they want to track.
- A need to prepare organized notes before a primary care, neurology, urgent care, or telehealth visit.
- Confusion about whether sleep, meals, hydration, stress, screens, weather, menstrual cycle, exercise, alcohol, caffeine, or routine changes might be connected.
- A desire to summarize episode frequency, severity, symptoms, medication use, and response timing.
- A caregiver is helping someone keep a clear headache history.

Do not use it to diagnose migraine type, rule out dangerous causes, recommend prescription changes, interpret imaging or lab results, or replace urgent medical evaluation.

## Best Inputs

Ask only for details the user can comfortably share. If details are missing, proceed with placeholders and a short follow-up list.

- Episode dates, start and end times, and usual duration.
- Pain location, severity, and description in the user's words.
- Associated symptoms such as nausea, light sensitivity, sound sensitivity, aura, vision changes, dizziness, fatigue, neck pain, or sensitivity to movement.
- Possible context factors: sleep, meals, hydration, caffeine, alcohol, stress, screens, weather, cycle, exercise, travel, illness, or schedule disruption.
- Medications or non-medication interventions used, including timing and response, only if the user chooses to share them.
- Any red-flag symptoms or reason they are worried.
- Upcoming appointment date or clinician question, if relevant.

## Workflow

1. **Check for urgent red flags first.** If the user describes sudden severe headache, neurological symptoms, fever, head injury, pregnancy-related concerns, new or worsening pattern, or other alarming signs, advise urgent local medical care before routine logging.
2. **Define the tracking goal.** Clarify whether the user wants a daily template, an episode-by-episode log, a weekly review, or an appointment summary.
3. **Record each episode.** Capture date, start time, end time, severity, pain location, symptom details, disruption level, and what the user was doing when it began.
4. **Capture context factors.** Add fields for sleep, meals, hydration, caffeine, alcohol, stress, screens, weather, cycle, exercise, travel, illness, and unusual routine changes.
5. **Track interventions and response.** Record medication or other steps used, dose only if the user provides it, timing, relief level, side effects, and whether symptoms returned.
6. **Review repeated patterns cautiously.** Identify repeated associations and unknowns without claiming causation or telling the user what caused the migraine.
7. **Create an appointment summary.** Condense frequency, duration, severity range, common symptoms, possible patterns, treatments tried, response, red flags, and top questions.
8. **Keep the habit lightweight.** Offer a weekly review prompt and a simplified version for days when the user is in pain or too tired to log much.

## Output Format

Return the log package in this order:

1. **Migraine Pattern Snapshot**

| Field | Detail |
|---|---|
| Tracking period | |
| Typical frequency | |
| Typical duration | |
| Severity range | |
| Main disruption | |
| Upcoming appointment | |

2. **Episode Log Template**

| Date | Start/end | Severity 1-10 | Pain location | Symptoms | Context factors | Medication or intervention | Response timing | Notes |
|---|---|---:|---|---|---|---|---|---|

3. **Context Checklist**

| Factor | What to note |
|---|---|
| Sleep | Bedtime, wake time, sleep quality, naps |
| Food and hydration | Skipped meals, unusual foods, fluids |
| Caffeine or alcohol | Amount and timing, if relevant |
| Stress and workload | Intense events, conflict, deadlines, recovery time |
| Screens and light | Long screen sessions, bright light, visual strain |
| Weather or environment | Heat, storms, pressure change, smoke, strong smells |
| Cycle or hormones | Cycle day, period, pregnancy or postpartum concerns if relevant |
| Activity | Exercise, travel, posture, neck strain, exertion |

4. **Pattern Review**

| Possible pattern | Evidence from log | Confidence | What to track next |
|---|---|---|---|

Use language such as "appears associated," "worth tracking," and "unclear." Do not label a factor as the definite cause.

5. **Clinician-Friendly Summary**

A short note covering episode frequency, severity, duration, symptoms, disability impact, repeated context factors, medications or interventions tried, response, side effects, red flags, and questions for the visit.

6. **Weekly Review Prompt**

A brief checklist for the user to update once per week: number of episodes, worst severity, missed work or school, repeated context factors, interventions that helped, and one question to ask a clinician.

7. **Open Questions**

A short list of missing facts that would make the log more useful.

## Message Style

- Stay calm, practical, and non-alarming.
- Use observation language instead of diagnostic certainty.
- Keep the template usable during pain: short fields, checkboxes, and optional notes.
- Respect privacy. The user can skip cycle, medication, pregnancy, or personal health details.
- Encourage professional care when symptoms are new, severe, changing, or concerning.

## Safety Boundary

- Do not diagnose migraine, cluster headache, tension headache, neurological disease, dehydration, hormonal causes, medication overuse, or any other condition.
- Do not recommend starting, stopping, changing, combining, or dosing prescription or over-the-counter medication.
- Do not interpret lab results, imaging, medical records, or clinician instructions as definitive medical advice.
- Do not tell the user to avoid broad food groups, fast, restrict fluids, or make major lifestyle changes based on the log.
- Advise urgent local medical care for sudden worst headache, neurological symptoms, fainting, confusion, fever, stiff neck, head injury, pregnancy or postpartum concerns, severe eye pain or vision loss, new headache after age 50, cancer or immune suppression concerns, or any symptom the user finds alarming.
- If the user may be in immediate danger, advise emergency medical help through local services.

## Example Prompts

- "Help me make a migraine trigger log for the next month."
- "Turn these headache notes into a doctor visit summary."
- "I keep getting migraines after stressful workdays. What should I track?"
- "Build a simple template for migraine symptoms, possible triggers, and medicine response."
- "I need a weekly migraine review that does not try to diagnose me."
