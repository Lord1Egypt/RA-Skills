## Description:

Goal Manager helps Chinese-speaking users create OKR and SMART goals, track progress, and generate periodic review templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking users and agent operators use this skill to create goals from built-in OKR/SMART templates, update key result progress, view saved goals, and generate daily, weekly, monthly, quarterly, or yearly review prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Goal data and reviews are stored in JSON files beside the skill when the helper runs.

Mitigation: Use it only in a workspace where local file persistence is acceptable, and avoid storing sensitive personal goals unless the workspace storage is trusted.

Risk: Delete or cancel requests may remove matching goals without a confirmation step.

Mitigation: Review goal names before issuing delete or cancel requests, and keep backups of goals.json if the data matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/skills/goal-manager)
- [ClawHub publisher profile](https://clawhub.ai/user/cp3d1455926-svg)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files]

**Output Format:** [Chinese Markdown responses and local JSON goal or review records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When executed, the Python helper stores goals and reviews in JSON files beside the skill.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
