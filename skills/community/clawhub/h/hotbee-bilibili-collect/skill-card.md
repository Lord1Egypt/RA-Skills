## Description:

Use when a user wants to parse or collect Bilibili video data through HotBee from a bilibili.com or b23.tv URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shanye1402-hash](https://clawhub.ai/user/shanye1402-hash)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect video data from a public Bilibili or b23.tv URL through HotBee after confirming any live API call and quota use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to run mutable remote GitHub CLI code that can access a local HotBee API key.

Mitigation: Use a restricted environment, minimal filesystem and environment access, and a low-privilege rotatable HotBee API key.

Risk: The referenced CLI transport sends the API key as a URL query parameter.

Mitigation: Redact signed query parameters from logs and errors, and prefer a version that sends credentials in headers or request bodies.

Risk: Live collection calls may consume HotBee quota or interact with third-party service limits.

Mitigation: Confirm user intent before live calls and only process public URLs explicitly supplied by the user.

## Reference(s):

- [Bilibili Collect API](references/api.md)
- [HotBee Skills](https://www.hotbee.cn/skills)
- [ClawHub skill page](https://clawhub.ai/shanye1402-hash/skills/hotbee-bilibili-collect)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and returned Bilibili video data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HOTBEE_API_KEY and a user-supplied public Bilibili or b23.tv URL.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
