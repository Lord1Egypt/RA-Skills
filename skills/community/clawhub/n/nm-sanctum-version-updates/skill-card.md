## Description:

Bumps versions, updates changelogs, and coordinates version changes across files for releases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to prepare project releases by coordinating semantic version changes across package manifests, changelogs, and README or other version references, then reviewing the updates. It expects repository changes to be captured first with the Sanctum git workspace review skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The partial security review could not resolve local references, leaving some referenced behavior unassessed.

Mitigation: Review the skill's local references and assess whether its version, release, and changelog triggers overlap with your workflows before installing.

## Reference(s):

- [Night Market Sanctum plugin page](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)

## Skill Output:

**Output Type(s):** [Configuration, Markdown, Shell commands]

**Output Format:** [Updated project configuration and Markdown documentation, with shell commands for verification.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Five ordered progress checkpoints for release preparation.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
