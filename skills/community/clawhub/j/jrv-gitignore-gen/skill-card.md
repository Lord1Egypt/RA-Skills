## Description:

Generate .gitignore files for any project type using GitHub's 200+ official templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, print, append, or overwrite .gitignore files from GitHub templates, combine multiple templates, add custom ignore rules, and detect likely project template needs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts GitHub to fetch template lists and template contents.

Mitigation: Use it only where outbound GitHub API access is acceptable, and review network policy before running commands that list or generate templates.

Risk: Generated output can overwrite, append to, or write a .gitignore file at a custom path.

Mitigation: Review the target path and use stdout preview mode before writing; use overwrite or append flags only when the file change is intended.

Risk: The skill caches the GitHub template list in the user's home cache directory.

Mitigation: Confirm local cache writes are acceptable for the execution environment or clear the cache after use if required.

## Reference(s):

- [GitHub gitignore templates API](https://api.github.com/gitignore/templates)
- [ClawHub skill page](https://clawhub.ai/johnnywang2001/skills/jrv-gitignore-gen)
- [Publisher profile](https://clawhub.ai/user/johnnywang2001)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and generated .gitignore text or files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write or append .gitignore files, print generated content to stdout, list template names, and cache GitHub template metadata locally.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
