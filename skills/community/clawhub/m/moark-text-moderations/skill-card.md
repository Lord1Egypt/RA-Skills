## Description:

Perform text review on user-specified input text that may be inappropriate or offensive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fchange](https://clawhub.ai/user/fchange)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to moderate user-provided text with the Gitee AI moderation API and present the moderation result with a brief summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided text is sent to Gitee AI for moderation, which can expose sensitive or regulated content to an external service.

Mitigation: Avoid submitting secrets or sensitive personal data unless authorized, and apply the organization's data handling policy before moderation.

Risk: The API key can be provided on the command line, where it may be captured in shell history or process listings.

Mitigation: Prefer GITEEAI_API_KEY from a protected environment or secret manager instead of passing --api-key.

Risk: The artifact declares an unpinned openai dependency, which can change behavior in controlled environments.

Mitigation: Pin and review the openai package version when deploying in production or regulated environments.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/fchange/skills/moark-text-moderations)
- [Publisher profile](https://clawhub.ai/user/fchange)
- [Gitee AI API endpoint](https://ai.gitee.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summary with extracted moderation JSON from command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GITEEAI_API_KEY or an --api-key argument and sends submitted text to Gitee AI for moderation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
