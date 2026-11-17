## Description:

This skill helps agents resolve Douyin video download links and optionally extract text from the video through Jiuma's remote service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dddcn1](https://clawhub.ai/user/dddcn1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn a Douyin video or share link into a resolved video download URL, then optionally submit and poll a Jiuma text-extraction task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided Douyin links, resolved video URLs, and task IDs are sent to Jiuma's remote service for processing.

Mitigation: Use the skill only with links that are appropriate to share with Jiuma, and avoid private, sensitive, or tracking-bearing URLs unless the service is trusted for that data.

Risk: Text extraction depends on remote service availability and task completion status.

Mitigation: Check task status before relying on extracted content, and handle failed or still-processing responses in the agent workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dddcn1/skills/jiuma-free-video-to-text)
- [Jiuma API endpoint](https://api.jiuma.com)

## Skill Output:

**Output Type(s):** [text, shell commands, API calls, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-like command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns resolved video URLs, download URLs, task IDs, task status, or extracted text depending on the selected action.]

## Skill Version(s):

1.0.4 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
