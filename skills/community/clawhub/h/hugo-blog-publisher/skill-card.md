## Description:

Publishes Markdown articles to a Hugo blog by generating front matter, adding a summary marker, creating taxonomy mapping files when needed, committing changes, and pushing to GitHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanteng](https://clawhub.ai/user/tanteng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and site maintainers use this skill to publish Markdown posts into a local Hugo blog repository and push the resulting changes to GitHub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local memory or configuration to discover blog settings.

Mitigation: Provide the blog path and domain explicitly, and review any discovered configuration before using it.

Risk: The skill can write files, commit changes, and push to GitHub without an explicit review gate.

Mitigation: Manually review generated files, target repository, branch, remote, commit message, and final push before allowing git commands to run.

## Reference(s):

- [Hugo Blog Front Matter Templates](artifact/references/frontmatter-templates.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with YAML front matter and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify Hugo content files and taxonomy mapping files before proposing git commit and push commands.]

## Skill Version(s):

1.1.1 (source: server release evidence; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
