## Description:

CSS Dead Code audits CSS, Sass, Less, Tailwind, Bootstrap, and CSS Modules projects by comparing selectors against template and component files, then reporting unused selectors, duplicate definitions, !important overuse, orphaned blocks, estimated byte savings, and verification commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and frontend engineers use this skill to audit project stylesheets for dead selectors, duplicate rules, orphaned CSS modules or animation blocks, and size-reduction opportunities before cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill scans broad project source files and may suggest deleting CSS files or removing rules.

Mitigation: Run it in a clean version-controlled workspace and manually review every selector and deletion command before applying changes.

Risk: The skill may use unpinned npx tooling, which can execute versions that differ over time.

Mitigation: Prefer locally installed, lockfile-pinned Tailwind or Percy binaries and inspect any npx command before running it.

## Reference(s):

- [Canlah AI homepage](https://canlah.ai)
- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-css-dead-code)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file paths, estimated byte savings, safe-deletion plans, and grep verification commands.]

## Skill Version(s):

1.0.3 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
