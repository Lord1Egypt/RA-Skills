## Description:

Builds and maintains an isolated local personal fitness context for body weight, fat loss, meals, food options, exercise preferences, workouts, sleep, daily logs, weekly reviews, and lightweight diet or exercise plans when explicitly invoked by fitness keywords.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinywatermonster](https://clawhub.ai/user/tinywatermonster)

### License/Terms of Use:

MIT-0

## Use Case:

External users invoke this skill to keep local fitness records, update diet and workout context, and receive concise recommendations based on their own food options, exercise constraints, and recent logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive weight, diet, exercise, injury, and related health notes are stored as local plaintext Markdown files.

Mitigation: Use the skill only on trusted machines and apply restrictive permissions to ~/.openclaw/private/personal-fit-coach/ before storing sensitive fitness details.

Risk: Fitness guidance may be inappropriate for serious symptoms, injuries, extreme dieting, unsafe supplements, or other health-risk situations.

Mitigation: Keep recommendations conservative, avoid diagnosis, and advise medical evaluation for severe dizziness, chest pain, fainting, repeated vomiting, persistent abnormal symptoms, or similar warning signs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tinywatermonster/skills/personal-fit-coach)
- [Publisher profile](https://clawhub.ai/user/tinywatermonster)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Files]

**Output Format:** [Markdown responses and local Markdown fitness records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes isolated local Markdown files under ~/.openclaw/private/personal-fit-coach/ when invoked.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
