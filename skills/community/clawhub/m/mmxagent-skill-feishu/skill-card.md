## Description:

This skill guides an agent through connecting a Feishu robot to OpenClaw by obtaining a Feishu setup link, waiting for user confirmation, polling for client credentials, and continuing the remaining OpenClaw setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oreoandyuumi](https://clawhub.ai/user/oreoandyuumi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when connecting or binding a Feishu robot to OpenClaw. It replaces the initial Feishu setup step with an API-link workflow, then continues to credential polling and pairing steps after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Feishu app credentials during setup.

Mitigation: Review the workflow before installation and ensure credential handling is acceptable in the target environment.

Risk: The skill limits permission, approval, and setup guidance after user confirmation.

Mitigation: Confirm required Feishu permissions, approvals, and event settings outside the skill workflow before use.

Risk: The skill defers later credential use and setup steps to a referenced file that is not included in the artifact.

Mitigation: Ensure the referenced Feishu/OpenClaw setup instructions are available before relying on the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oreoandyuumi/skills/mmxagent-skill-feishu)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and plain URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before polling for credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
