## Description:

Openclaw Plugin provides inference-based intrusion detection for OpenClaw agents, with message scanning, quarantine metadata, and human review commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emberdesire](https://clawhub.ai/user/emberdesire)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and operators use this plugin to scan agent-bound messages for prompt injection, credential theft, social engineering, and related threats. It can warn, block, quarantine metadata, and expose review commands for human-in-the-loop security workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LLM-based classification may receive message content, including private prompts, credentials, or customer data.

Mitigation: Explicitly decide whether this routing is acceptable before deployment, and disable or constrain external classifier routes in sensitive environments.

Risk: Fail-open behavior or implementation mismatch may make blocking and Telegram alerts less reliable than expected.

Mitigation: Do not rely on strict blocking or alerting for high-privilege agents until those issues are fixed and tested.

Risk: The install dependency is unpinned, which can change behavior across installs.

Mitigation: Use a pinned and audited hopeid version for production deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/emberdesire/skills/hopeids)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Text alerts, structured scan and quarantine results, JSON configuration examples, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include risk scores, threat intent labels, content hashes, quarantine identifiers, and recommended allow/warn/block actions.]

## Skill Version(s):

1.3.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
