## Description:

Generate commit messages from diffs, write PR descriptions, create changelogs, suggest branch names. Every git workflow, automated.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to draft Git workflow text from local repository changes, including commit messages, pull request descriptions, changelogs, and branch names.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local Git diffs and commit history may contain proprietary code or sensitive changes.

Mitigation: Use the skill only in repositories where local diff and history access is acceptable, and confirm any configured AI provider before sending sensitive content outside the local environment.

Risk: Generated commit messages, pull request descriptions, changelogs, or branch names may be incomplete or misleading.

Mitigation: Review generated Git workflow text before committing, publishing pull requests, or sharing release notes.

Risk: The skill reads repository state through Git commands and depends on the current working tree and branch context.

Mitigation: Run it from the intended repository and branch, and verify staged changes or base branches before using generated output.

## Reference(s):

- [GitAssist ClawHub skill page](https://clawhub.ai/theshadowrose/skills/git-assist)
- [Publisher profile](https://clawhub.ai/user/theshadowrose)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Plain text, Markdown, and JSON-formatted CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated from local Git diffs, branch history, and user-provided branch descriptions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
