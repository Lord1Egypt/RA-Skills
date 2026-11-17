## Description:

Skill Builder helps agents decide whether reusable skill guidance is warranted, draft minimal SKILL.md skeletons, and audit existing skills for bloat, trigger quality, and scope drift.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zurbrick](https://clawhub.ai/user/zurbrick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent maintainers use this skill to decide, create, or tighten OpenClaw-style skill packages while keeping workflows minimal and focused.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated trigger descriptions may be broader than intended and cause the skill to activate too often.

Mitigation: Review proposed trigger descriptions against realistic clear-trigger, edge-case, and near-miss prompts before publishing.

Risk: Generated skill skeletons or audit recommendations may lead to file edits or new scripts in a workspace.

Mitigation: Approve actual file changes and script additions through the normal review workflow before applying them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zurbrick/skills/lean-skill-builder)
- [Decision Tree](references/decision-tree.md)
- [Frontmatter Patterns](references/frontmatter-patterns.md)
- [Writing Patterns](references/writing-patterns.md)
- [Supporting Files Guide](references/supporting-files-guide.md)
- [Audit Checklist](references/audit-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with plain text recommendations, folder trees, YAML frontmatter, and SKILL.md outlines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Leads with a recommendation and keeps build or audit output to the smallest justified package.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
