## Description:

Manage PARA-based personal knowledge management (PKM) systems using the Projects, Areas, Resources, and Archives organization method.

This skill is ready for commercial/non-commercial use.

## Publisher:

[killerapp](https://clawhub.ai/user/killerapp)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to create, organize, validate, navigate, and archive PARA-based personal knowledge bases. It supports developers, consultants, researchers, product builders, and career professionals who need action-oriented note organization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts can overwrite, create, or delete files outside the intended knowledge-base path when given crafted paths.

Mitigation: Run scripts only with trusted KB-local paths, avoid absolute paths and '..' components, and review --output destinations before execution.

Risk: Archiving moves project content and removes the original project file after writing the archive copy.

Mitigation: Use backups or version control for important notes before archiving completed projects.

## Reference(s):

- [PARA Method Principles](references/para-principles.md)
- [PARA Decision Guide](references/decision-guide.md)
- [Common PARA Patterns](references/common-patterns.md)
- [AI Navigation Best Practices](references/ai-navigation.md)
- [Fortelabs PARA Method](https://fortelabs.com/blog/para/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update knowledge-base folders, README.md, AGENTS.md, archive files, and validation output when helper scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
