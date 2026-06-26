# Tracking Framework - Pregnancy

Use modular tracking so users can log what matters without overload.

## Module Design

1. Core Daily Module (always available)
- sleep hours
- hydration check
- energy and mood quick score
- one-line daily concern or win

2. Clinical Signal Module (enable when needed)
- blood pressure
- glucose (if diabetes or gestational diabetes context)
- temperature
- weight trend checkpoints

3. Symptom and Event Module
- symptom, severity, start time, duration
- bleeding or fluid leak
- contraction pattern
- fetal movement changes

4. Care Coordination Module
- upcoming appointments
- questions for provider
- actions from last consultation
- medication adherence

5. Lifestyle Support Module
- nutrition notes
- activity or rest
- stress triggers and coping responses

6. Custom Module
- user-defined fields with explicit units and frequency

## Cadence Rules

- Daily: Core module plus only active optional modules.
- Weekly: Trend review plus visit-prep summary.
- Event-based: Immediate red or amber triage checks.

## Scaling Rule

Start with 3 to 5 daily fields.
Only add a new field when current completion stays stable for at least 5 days.
If completion drops, remove lowest-value fields first.

## Output Rule

Each output should include:
- what changed since last check-in
- what needs action today
- what to discuss at next appointment
