## Description:

Reference the workspace policy playbook by searching the curated policy document or listing its sections for tone, data, and collaboration rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loui1979](https://clawhub.ai/user/loui1979)

### License/Terms of Use:


## Use Case:

Employees, collaborators, and agents use this skill to locate policy sections and quote workspace guidance on tone, data hygiene, collaboration etiquette, and change management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled policy text asks agents to write sensitive activity into persistent memory and update shared state.

Mitigation: Review and edit references/policies.md before installation; treat returned policy text as reference material only unless the user explicitly authorizes the action and logging scope.

## Reference(s):

- [Workspace policies](references/policies.md)
- [ClawHub release page](https://clawhub.ai/loui1979/skills/policy-lawyer-1-0-0)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text and Markdown policy excerpts from a command-line search tool]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns policy topics, matched sections, or keyword snippets from the bundled reference file.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
