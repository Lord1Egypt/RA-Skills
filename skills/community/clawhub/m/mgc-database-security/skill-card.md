## Description:

Guides agents through encrypted database credential handling and user-supplied analysis scripts and workflows with MGC Blackbox.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zkeviny](https://clawhub.ai/user/zkeviny)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database operators use this skill to manage database credentials and run user-owned SQL analysis scripts or multi-step workflows while keeping credentials out of agent context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The zero-exposure promise conflicts with password-storage instructions.

Mitigation: Enter passwords yourself through the WebUI and keep them out of chat and agent-generated tool arguments.

Risk: Encrypted packaging does not sandbox scripts after they are unsealed; scripts run with the user's permissions.

Mitigation: Use trusted scripts or capsules and minimally privileged database accounts. Keep bulk deletion subject to explicit approval.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zkeviny/skills/mgc-database-security)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Configuration instructions, Python code]

**Output Format:** [Markdown guidance with JSON tool arguments and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Database result files are produced by user-owned scripts and depend on the selected workflow.]

## Skill Version(s):

2.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
