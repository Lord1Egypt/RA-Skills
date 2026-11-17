## Description:

Reviews AI short-film and storyboard image/video prompts against a ten-point checklist for time marking, subject consistency, scene anchors, lighting, shadows, material consistency, depth, shot type, shadow direction, and asset references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beermanzz](https://clawhub.ai/user/beermanzz)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, prompt reviewers, and storyboard teams use this skill to preflight image and video generation prompts before batch production or review handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Strict checklist feedback may reject prompts that are intentionally experimental or stylistically loose.

Mitigation: Use the checklist as a production quality gate and allow human reviewers to override failures when a prompt intentionally departs from the listed constraints.

Risk: The skill expects concrete asset-path conventions; teams without stable asset references may receive incomplete or repetitive remediation guidance.

Mitigation: Establish character, location, prop, and costume reference naming conventions before using the checklist for batch prompt review.

## Reference(s):

- [Prompt Quality Checklist Detailed Reference](references/checklist-detailed.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, text]

**Output Format:** [Markdown checklist guidance with pass/fail review criteria and prompt revision examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language checklist content with bilingual prompt-quality terminology.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
