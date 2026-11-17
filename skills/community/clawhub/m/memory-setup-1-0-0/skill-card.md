## Description:

Enables and configures Moltbot/Clawdbot memory search with guidance for MEMORY.md, daily logs, provider setup, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gwsq](https://clawhub.ai/user/gwsq)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to set up persistent memory search for Moltbot/Clawdbot agents, including configuration, workspace memory structure, daily logs, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memory and session indexing can expose private, confidential, regulated, or credential-bearing content to the selected embedding provider.

Mitigation: Review what will be indexed before installation, avoid storing secrets or regulated data, and use an approved provider and retention policy.

Risk: The default guidance recommends remote embedding providers for memory search, which may not fit sensitive workflows.

Mitigation: Prefer the local provider or memory-only sources when handling sensitive work or when provider approval is not established.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gwsq/skills/memory-setup-1-0-0)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown with JSON configuration examples, shell commands, and file structure examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides setup and troubleshooting guidance; does not execute commands directly.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
