## Description:

Neta API community skill for browsing interactive feeds, viewing collection details, interacting with works, and browsing content by tags and characters in a community context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huxiuhan](https://clawhub.ai/user/huxiuhan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to browse Neta community works, inspect collection details, discover tag and character context, and perform account interactions such as likes, favorites, comments, and follows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses authenticated Neta CLI access and can affect a user's community account through likes, favorites, comments, and follows.

Mitigation: Use a minimally scoped token where available and confirm every account-affecting action before execution.

Risk: The installation guidance uses an unpinned global CLI package install.

Mitigation: Prefer a pinned, locally installed CLI version and verify the installed package before use.

Risk: Authenticated API responses may include account or community data that should not be exposed in shared files or logs.

Mitigation: Avoid saving authenticated responses in shared temporary paths and keep debug logging narrow.

## Reference(s):

- [Neta Community on ClawHub](https://clawhub.ai/huxiuhan/skills/neta-community)
- [Best Practices for Interactive Feed](artifact/references/interactive-feed.md)
- [Social Interaction Skills](artifact/references/social-interactive.md)
- [Best Practices for Hashtag Research](artifact/references/hashtag-research.md)
- [Best Practices for Character Search](artifact/references/character-search.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose authenticated Neta CLI commands that affect the user's community account.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
