## Description:

Creates a clinician-friendly migraine or recurring headache pattern log with episode timelines, possible context factors, symptom notes, medication response tracking, red-flag guidance, and a concise appointment summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and caregivers use this skill to organize recurring migraine or headache observations into a lightweight log, cautious pattern review, and clinician-friendly visit summary. It supports tracking and appointment preparation without diagnosing conditions or recommending treatment changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may share sensitive health details while building the log.

Mitigation: Prompt users to share only information they are comfortable sharing and allow them to skip cycle, medication, pregnancy, or other personal health fields.

Risk: Users may treat the log or pattern review as diagnosis or medical advice.

Mitigation: Frame outputs as tracking support only, use cautious association language, avoid claims of causation, and encourage clinician review for new, changing, or concerning symptoms.

Risk: Severe or alarming symptoms could be delayed by routine logging.

Mitigation: Check for urgent red flags first and direct users to urgent local medical care for sudden severe headache, neurological symptoms, fever, injury, pregnancy-related concerns, severe eye pain or vision loss, or other alarming symptoms.

Risk: Medication notes could be misused to infer dosing or treatment changes.

Mitigation: Record medication or intervention details only when the user provides them, and avoid recommending starting, stopping, changing, combining, or dosing medication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/migraine-trigger-pattern-log)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown tables and concise prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only output; no code execution, network access, credentials, or persistence.]

## Skill Version(s):

1.0.1 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
