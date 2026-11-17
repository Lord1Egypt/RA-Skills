## Description:

Turns a project folder into a polished public open-source repository by improving documentation, community files, repository metadata, and Git/GitHub setup while preserving source code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openghz](https://clawhub.ai/user/openghz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to prepare local projects for public open-source release by improving repository documentation, community health files, metadata, and Git/GitHub setup without changing product source code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and push to a public GitHub repository, which may expose private files, secrets, or Git history if performed without sufficient review.

Mitigation: Require explicit confirmation of the GitHub account, repository name, public visibility, branch or ref, and the results of a full secret and history review before any GitHub action.

Risk: Repository polishing can accidentally publish local paths, private project details, or misleading documentation.

Mitigation: Limit changes to documentation and repository metadata, use placeholders or relative paths, and review public-facing Markdown before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openghz/skills/open-source-project-polish)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and repository file changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May add or update documentation, community files, repository metadata, Git configuration, and GitHub repository settings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
