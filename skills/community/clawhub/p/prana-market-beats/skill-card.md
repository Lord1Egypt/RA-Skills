## Description:

Market Beats Prana forwards user requests to a remote Prana market-beats service that returns real-time financial news updates from sources such as Jin10.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyffeifeifei](https://clawhub.ai/user/cyffeifeifei)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and channel integrators use this skill to request real-time financial news updates through a Prana-hosted service and pass the returned result through to the end user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is presented as a real-time financial news tool, but the artifact is a remote Prana client that forwards user prompts and credentials to a selected service.

Mitigation: Use only a trusted Prana endpoint, avoid overriding the base URL unless you control the destination, and do not send sensitive prompts.

Risk: The thin clients may fetch API credentials and store them in config/api_key.txt by default.

Mitigation: Prefer environment-provided credentials and set PRANA_SKILL_SKIP_WRITE_API_KEY=1 or PRANA_SKILL_NO_AUTO_API_KEY=1 to avoid plaintext credential storage.

Risk: The package does not contain the market-news implementation, so output quality and availability depend on the remote Prana service.

Mitigation: Disclose the remote-service dependency and review returned news before using it in financial monitoring workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyffeifeifei/skills/prana-market-beats)
- [Artifact README](artifact/README.md)
- [Artifact skill manifest](artifact/skill.yaml)

## Skill Output:

**Output Type(s):** [text, json]

**Output Format:** [JSON returned by the Prana agent-run or agent-result API and passed through by the thin client]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The output depends on the remote Prana endpoint, credentials, and the user's request.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; artifact skill.yaml declares 8.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
