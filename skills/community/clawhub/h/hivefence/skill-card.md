## Description:

Collective immunity network for AI agents. When one agent detects a prompt injection attack, all connected agents become immune. Real-time pattern detection, community voting, and distributed threat intelligence. Built on top of prompt-guard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seojoonkim](https://clawhub.ai/user/seojoonkim)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use HiveFence to add prompt-injection detection, threat reporting, community voting, and distributed threat-intelligence updates to AI-agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic reporting may send prompt-derived threat hashes to an external service.

Mitigation: Install only where outbound threat-hash reporting is acceptable, and confirm whether automatic reporting can be disabled before use with confidential prompts.

Risk: Installation examples do not pin package versions.

Mitigation: Use a pinned package version or verified release before deploying in production workflows.

## Reference(s):

- [HiveFence Website](https://hivefence.com)
- [HiveFence API Docs](https://hivefence.com/docs)
- [HiveFence API Base URL](https://hivefence-api.seojoon-kim.workers.dev)
- [VittoStack Security Guide](https://x.com/vittostack/status/2018326025373900881)
- [ZeroLeaks Security Assessment](https://x.com/NotLucknite/status/2017665998514475350)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with bash and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API endpoint references, installation commands, and defensive integration guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
