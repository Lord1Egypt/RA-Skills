## Description:

Self-Learning for Noktasist guides an agent to document discoveries, debugging outcomes, tool usage, and long-term memory updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noktanyus](https://clawhub.ai/user/noktanyus)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers running Noktasist use this skill to guide an agent through learning from new systems, errors, tools, and operational observations while updating memory and related project files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to persist broad memory, user, identity, logs, configuration, and repository changes without clear consent or scope limits.

Mitigation: Require explicit user approval before writing long-term memory, USER.md, IDENTITY.md, SOUL.md, logs, configs, or git commits.

Risk: Memory and log updates could capture secrets, personal data, raw logs, or unrelated files.

Mitigation: Prohibit storing secrets, personal data, raw logs, and unrelated files in persistent memory or repository updates.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with ordered checklists, a file-update table, and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct edits to memory, user, identity, log, config, and git state; review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
