## Description:

A Chinese-language code and system review skill that guides agents through correctness, readability, architecture, security, performance, Agent Skill supply-chain checks, BIV review, and MCP Server security auditing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqyougitcom](https://clawhub.ai/user/qqyougitcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to review pull requests, implementation plans, refactors, bug fixes, Agent Skills, and MCP Servers before merge, installation, or deployment. It helps structure findings by severity and review axis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may surface security-sensitive search commands and review prompts that could be misread as operational instructions.

Mitigation: Use the commands as read-only audit checks and confirm any proposed action before changing code, credentials, deployments, or MCP Server configuration.

Risk: Review checklists can produce overbroad or incorrect findings when the agent lacks repository context.

Mitigation: Require findings to cite concrete files, behavior, or tests, and have a human reviewer confirm Critical and Important issues before blocking release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qqyougitcom/skills/mimo-code-review-and-quality)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with checklists, tables, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language review structure with severity labels and security audit checklists.]

## Skill Version(s):

1.4.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
