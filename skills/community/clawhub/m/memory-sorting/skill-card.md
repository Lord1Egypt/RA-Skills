## Description:

Organizes an agent memory store by scanning MEMORY.md, topics, and daily notes for duplicate, outdated, conflicting, orphaned, fragmented, or oversized content, then producing reviewable cleanup proposals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jofiction918](https://clawhub.ai/user/jofiction918)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to audit and reorganize persistent agent memory files. It produces a structured cleanup proposal for human approval before modifying memory content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to inspect broad persistent memory files and may propose edits or deletions.

Mitigation: Review every proposed change before approval, especially deletions, and make backups before execution.

Risk: Incorrect cleanup proposals could remove useful context or preserve misleading memory content.

Mitigation: Approve only specific numbered changes after checking the affected files and review the execution report after edits are applied.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jofiction918/skills/memory-sorting)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown proposal and execution report with optional shell commands for duplicate or conflict searches]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires human approval before executing proposed memory edits or deletions.]

## Skill Version(s):

3.0.7 (source: server release metadata; artifact frontmatter says 3.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
