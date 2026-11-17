## Description:

Post updates to LinkedIn, track analytics, and optimize content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yadavabhijeet4](https://clawhub.ai/user/yadavabhijeet4)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to draft, preview, publish, and analyze LinkedIn posts through helper scripts and configured LinkedIn OAuth credentials. It can also request Gemini feedback or generate draft content from local research notes when a Gemini API key is provided.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpublished draft content and local research notes may be sent to Gemini when draft generation or feedback features are used.

Mitigation: Use non-sensitive drafts unless external processing is acceptable, and run preview with the feedback feature disabled when local-only behavior is needed.

Risk: LinkedIn access tokens may be printed in plaintext during token generation.

Mitigation: Avoid sharing terminal output from token generation and rotate any LinkedIn token that was printed, logged, or exposed.

Risk: The security evidence marks the release as suspicious.

Mitigation: Review the skill before installing or executing it, with particular attention to credential handling and external API calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yadavabhijeet4/skills/linkedin-ai-optimizer)
- [LinkedIn Developers Apps](https://www.linkedin.com/developers/apps)
- [LinkedIn OAuth authorization endpoint](https://www.linkedin.com/oauth/v2/authorization)
- [LinkedIn OAuth access token endpoint](https://www.linkedin.com/oauth/v2/accessToken)
- [Gemini GenerateContent endpoint](https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Files, Guidance]

**Output Format:** [Console text, Markdown feedback, JSON analytics responses, and local JSONL or draft text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preview mode is default for posting; publishing requires an explicit confirmation flag.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
