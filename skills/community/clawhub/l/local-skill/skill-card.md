## Description:

Local skill repository for publish and pre-publish inspection that provides inspectSkill and summarizeSkill utilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[li-chi](https://clawhub.ai/user/li-chi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release maintainers use this skill to inspect a local skill package, summarize its metadata, and run pre-publish checks before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running release workflow scripts without checking the package metadata can target the wrong package or version.

Mitigation: Review the package metadata and scripts, then run the publish script from the repository root only after confirming the target package and version.

## Reference(s):

- [Release process](docs/release.md)
- [ClawHub skill page](https://clawhub.ai/li-chi/skills/local-skill)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local inspection summaries, package metadata checks, and dry-run publish guidance.]

## Skill Version(s):

0.2.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
