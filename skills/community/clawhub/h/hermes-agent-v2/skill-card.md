## Description:

Hermes Agent Skill integrates the NousResearch Hermes Agent CLI for agent workflows including persistent memory, sub-agent delegation, MCP integration, browser automation, and code execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wihy](https://clawhub.ai/user/wihy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to call Hermes CLI from an agent session for Q&A, context-aware runs, delegation, memory operations, skill management, status checks, and configuration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hermes CLI and its configured model provider may process prompts, context files, and delegated tasks outside this skill.

Mitigation: Use this skill only with a trusted Hermes CLI installation and trusted model provider configuration; avoid passing sensitive files with --context-file unless that processing is intended.

Risk: Memory notes, created skills, and ~/.hermes configuration changes can persist beyond a single run.

Mitigation: Periodically review Hermes memory notes, created skills, and ~/.hermes configuration for stale, sensitive, or unexpected state.

Risk: Broad Hermes agent capabilities, including delegation, browser automation, code execution, and MCP integration, may operate without clear approval boundaries.

Mitigation: Run Hermes in controlled workspaces, review commands before execution, and apply local sandbox or approval policies where available.

## Reference(s):

- [ClawHub Hermes Agent Skill](https://clawhub.ai/wihy/skills/hermes-agent-v2)
- [NousResearch Hermes Agent documentation](https://github.com/NousResearch/hermes-agent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local Hermes configuration and persistent Hermes memory state.]

## Skill Version(s):

2.1.1 (source: server release metadata; artifact frontmatter and _meta.json list 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
