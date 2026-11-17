## Description:

Treehole guides agents working on the PKU Treehole Rust CLI, including forum commands, authentication flows, and schedule or calendar queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjsoj](https://clawhub.ai/user/wjsoj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers maintaining or debugging the Treehole CLI use this skill to understand command behavior, API flows, authentication/session handling, and schedule or calendar features.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to access a PKU account using stored keyring credentials and an SMS code from the environment.

Mitigation: Require explicit confirmation before login, SMS verification, or account-data queries.

Risk: The skill covers actions that can change forum state, including posting, replying, voting, and following content.

Mitigation: Require explicit confirmation before any posting, replying, voting, or follow/unfollow action.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wjsoj/skills/pku-treehole)
- [Treehole API Docs](docs/treehole-api.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
