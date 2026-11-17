## Description:

Gitignore Sync generates context-aware .gitignore rules from requested templates and repository signals, backed by gitignore.io.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikita-holban](https://clawhub.ai/user/nikita-holban)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create or update a repository .gitignore from requested tooling and detected project files while preserving manual rules outside a managed block.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts gitignore.io through Toptal to fetch ignore templates.

Mitigation: Use dry-run to preview behavior or the local rules-file option when avoiding network access is preferred.

Risk: The skill modifies the repository .gitignore file.

Mitigation: Review the managed block after execution and keep manual rules outside the managed block markers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nikita-holban/skills/gitignore-sync)
- [gitignore.io API](https://www.toptal.com/developers/gitignore/api)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and repository file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Updates only a gitignore-sync managed block; supports dry-run and local rules-file modes.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
