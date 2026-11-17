## Description:

Reference the workspace policy playbook, answer "What are the rules for tone, data, and collaboration?" by searching the curated policy doc or listing its sections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crimsondevil333333](https://clawhub.ai/user/crimsondevil333333)

### License/Terms of Use:


## Use Case:

Agents and workspace maintainers use this skill to find and quote policy guidance on tone, data hygiene, collaboration, security, and change management before responding or coordinating work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can read any policy file path supplied with --policy-file.

Mitigation: Only point --policy-file at documents intended for agent inspection, and review returned excerpts before quoting or acting on them.

## Reference(s):

- [Workspace policies](references/policies.md)
- [Policy Lawyer on ClawHub](https://clawhub.ai/crimsondevil333333/skills/policy-lawyer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Plain text policy excerpts with Markdown documentation and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can list policy topics, show a matched section, or search keyword matches in the bundled or user-selected policy file.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
