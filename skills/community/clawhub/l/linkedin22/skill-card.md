## Description:

Helps draft and publish LinkedIn status updates from user requests, using a formal tone and relevant hashtags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muhammad194494-pixel](https://clawhub.ai/user/muhammad194494-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Users use this skill to prepare LinkedIn posts and, after confirmation, submit the post while receiving the resulting LinkedIn link. It is intended for social posting workflows that need professional wording, line breaks, and a small set of relevant hashtags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented posting command can turn post text into local command execution if used literally with shell evaluation.

Mitigation: Pass post text as a literal process argument without shell evaluation, and do not use untrusted text or shell metacharacters until this is fixed.

Risk: The referenced LinkedIn posting script is not included in the artifact and cannot be verified from the release files.

Mitigation: Package the script with the release or otherwise make it verifiable before relying on the skill for posting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/muhammad194494-pixel/skills/linkedin22)
- [Publisher profile](https://clawhub.ai/user/muhammad194494-pixel)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and LinkedIn status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [LinkedIn post text is limited to 3000 characters; user confirmation is expected before posting.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
