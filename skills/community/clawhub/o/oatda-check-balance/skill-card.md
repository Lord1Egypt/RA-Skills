## Description:

Check OATDA account balance, remaining credits, and total usage via the unified AI gateway before expensive image, video, or long-running LLM calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devcsde](https://clawhub.ai/user/devcsde)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check available OATDA credits, total spend, and top-up balance before starting expensive AI generation or long-running LLM work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads an OATDA API key from the environment or ~/.oatda/credentials.json to authenticate balance checks.

Mitigation: Provide OATDA_API_KEY through the normal secret mechanism, avoid printing the full key, and only verify key presence or a short prefix when needed.

Risk: Balance output can influence whether a user proceeds with paid or expensive AI generation work.

Mitigation: Use actualBalance as the remaining-budget value and re-check balance before high-cost or long-running calls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/devcsde/skills/oatda-check-balance)
- [OATDA Homepage](https://oatda.com)
- [OATDA Credits API](https://oatda.com/api/v1/user/credits)
- [OATDA Credits Dashboard](https://oatda.com/dashboard/credits)
- [OATDA API Keys Dashboard](https://oatda.com/dashboard/api-keys)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Markdown, Guidance]

**Output Format:** [Markdown with inline bash commands and a concise balance summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses OATDA_API_KEY from the environment or ~/.oatda/credentials.json; should not print full API keys.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
