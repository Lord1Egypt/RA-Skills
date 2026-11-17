## Description:

Zero-Knowledge Execution for Sensitive Agent Tasks - Privacy computing framework for AI Agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill for guidance, commands, configuration, and TypeScript examples for an AI-agent private computation framework that stores credentials, executes sensitive tasks, and records audit logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release advertises zero-knowledge execution, TEE isolation, and HIPAA/GDPR compliance, while security evidence says those protections are not implemented yet.

Mitigation: Do not rely on the skill for regulated, medical, financial, or other high-sensitivity workloads until the publisher provides the reviewed implementation, version pinning, key-management details, audit-log safeguards, and evidence that unavailable security modes fail closed.

Risk: The skill examples handle API keys and other secrets.

Mitigation: Review the actual credential storage and key-management implementation before installing or using it with real secrets.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhenstaff/skills/private-computation)
- [OpenClaw Private Computation Homepage](https://github.com/ZhenRobotics/openclaw-private-computation)
- [OpenClaw Private Computation Documentation](https://github.com/ZhenRobotics/openclaw-private-computation#readme)
- [Quick Start Guide](https://github.com/ZhenRobotics/openclaw-private-computation/blob/main/QUICKSTART.md)
- [Examples](https://github.com/ZhenRobotics/openclaw-private-computation/tree/main/examples)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline TypeScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API examples for credential storage, task execution, audit logging, and security-level configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
