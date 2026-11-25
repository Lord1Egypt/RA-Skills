## Description:

Detects git forge (GitHub/GitLab/Bitbucket) and maps CLI commands cross-platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to identify whether a repository is hosted on GitHub, GitLab, or Bitbucket and to choose equivalent commands and configuration patterns when working across those platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes GitHub Discussions searches and operations that may use account credentials to create or change content.

Mitigation: Before running a discussion operation, confirm the target repository, the requested change, and the account permissions being used.

Risk: The security scan had partial coverage because two referenced paths were not resolved.

Mitigation: Review the complete installed skill and its referenced files before relying on its guidance.

## Reference(s):

- [Project homepage listed in skill metadata](https://github.com/athola/claude-night-market/tree/master/plugins/leyline)
- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-leyline-git-platform)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with cross-platform command tables and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides command and configuration guidance for GitHub, GitLab, and Bitbucket workflows.]

## Skill Version(s):

1.10.4 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
