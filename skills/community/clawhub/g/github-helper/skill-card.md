## Description:

GitHub Helper helps agents search, clone, sync, and inspect local or remote GitHub repositories using a local knowledge base, GitHub CLI, and GitHub MCP fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dandandujie](https://clawhub.ai/user/dandandujie)

### License/Terms of Use:


## Use Case:

Developers and repository maintainers use this skill to manage local GitHub repository collections, keep a searchable CLAUDE.md knowledge base, and inspect repository issues, pull requests, releases, and local code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository README text can be persisted into CLAUDE.md and later used as agent context.

Mitigation: Use only trusted repository directories and inspect generated CLAUDE.md content before relying on it.

Risk: The skill can clone repositories and update the local repository knowledge base.

Mitigation: Confirm repository URLs and target directories before cloning or running knowledge base updates.

Risk: Environment-specific path changes may be written into SKILL.md.

Mitigation: Review any path edits before reuse and keep local configuration changes separate from release content where possible.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON output from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local CLAUDE.md repository knowledge base when helper scripts are run.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
