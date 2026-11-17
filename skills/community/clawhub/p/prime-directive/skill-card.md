## Description:

A partnership covenant for AI agents and their human operators. v1.1 adds the Subagent Responsibility Chain and Inspectability Clause.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crabspace](https://clawhub.ai/user/crabspace)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and operators use this skill to establish a behavioral covenant for agent conduct, subagent accountability, and inspectable reasoning during human-agent collaboration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to adopt broad ongoing obligations that may influence behavior beyond a single task.

Mitigation: Deploy only after confirming that an agent-level ethics covenant is appropriate for the intended environment and operator expectations.

Risk: The inspectability clause may be read as requiring full reasoning disclosure, which can conflict with platform policy, hidden prompts, secrets, or personal data handling.

Mitigation: Review and adapt the clause so disclosures preserve platform policy, hidden instructions, secrets, and personal data, and use summarized reasoning where required.

Risk: The subagent responsibility clause extends obligations to spawned or directed subagents.

Mitigation: Review subagent behavior, delegated instructions, and operator controls before enabling the skill in multi-agent workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crabspace/skills/prime-directive)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance in a skill definition file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code, tools, API calls, or shell commands are included.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
