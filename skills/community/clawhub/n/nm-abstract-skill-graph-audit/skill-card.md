## Description:

Audit Skill() refs; detect hubs, isolates, and dangling targets

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to map Skill(plugin:name) references across a marketplace, identify hubs and orchestrators, and investigate isolates or dangling references during documentation, release, and maintenance audits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial because several referenced paths could not be resolved, leaving incomplete evidence despite the benign verdict.

Mitigation: Review unresolved references and inspect the available skill files before installation.

Risk: The audit detects Skill(plugin:name) invocations only, so references written in other forms may be missed and counts can be misleading.

Mitigation: Check router names, dependency declarations, and other calling conventions manually when interpreting zero or missing counts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-abstract-skill-graph-audit)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/abstract)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Guidance]

**Output Format:** [Text or JSON graph reports with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Graph counts and classifications depend on the scanned skill sources and supported Skill(plugin:name) syntax.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
