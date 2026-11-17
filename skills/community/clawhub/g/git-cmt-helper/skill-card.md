## Description:

Generate standardized git commit messages following Conventional Commits format, including team conventions for type prefixes, module scopes, subject length, and breaking change documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xtresser](https://clawhub.ai/user/0xtresser)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to draft or validate git commit messages that follow Conventional Commits and project-specific module scopes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated commit messages may be inaccurate or omit important context from the actual code change.

Mitigation: Review each generated commit message before committing, as recommended by the security guidance.

Risk: The static module scope list may not match every repository that installs the skill.

Mitigation: Confirm the chosen scope against the project modules reference or update the scope list for the target repository.

## Reference(s):

- [Project Modules](references/modules.md)
- [ClawHub skill page](https://clawhub.ai/0xtresser/skills/git-cmt-helper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with Conventional Commits examples and inline git commit guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commit subjects are constrained to 72 characters including the type and scope prefix.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
