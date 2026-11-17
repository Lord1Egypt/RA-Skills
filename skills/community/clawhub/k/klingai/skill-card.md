## Description:

Generate Kling AI videos and images, manage reusable subjects and voices, and check account quotas through Kling's API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[klingai-dev](https://clawhub.ai/user/klingai-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative teams use this agent skill to generate videos and images with Kling AI, manage reusable subjects and voices, and review account quotas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording may lead the skill to be selected for loosely related requests.

Mitigation: Use it when the user clearly requests a Kling task, and clarify ambiguous requests before acting.

Risk: The security guidance notes that device metadata may be stored during account binding without clear disclosure.

Mitigation: Review Kling's binding and privacy terms before binding, and avoid binding from shared devices.

Risk: Generation tasks incur charges and send prompts and reference media to Kling AI.

Mitigation: Submit only when the user has clearly requested generation and understands the charges and media transfer.

## Reference(s):

- [Kling AI API documentation](https://klingai.com/document-api/)
- [Kling AI API authentication](https://klingai.com/document-api/api/get-started/authentication.md)
- [ClawHub skill release](https://clawhub.ai/klingai-dev/skills/klingai)

## Skill Output:

**Output Type(s):** [API Calls, Video, Images, Text, Configuration instructions]

**Output Format:** [Generated media files, quota and task responses, and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation tasks are billable; media outputs can be downloaded locally.]

## Skill Version(s):

2.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
