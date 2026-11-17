## Description:

Helps agents manage WeChat public-account RSS subscriptions and read subscribed WeChat and X content through the mp2rss CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[areyoubugcoder](https://clawhub.ai/user/areyoubugcoder)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents use this skill to subscribe to and manage WeChat public accounts, retrieve their articles, read posts and articles from subscribed X accounts, and manage mp2rss login. X account subscriptions must be changed in the web console.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation and updates can run code from mutable remote sources.

Mitigation: Review install and update paths; prefer pinned packages or release downloads with verified checksums instead of piping a mutable-branch script to a shell.

Risk: Skill synchronization during updates can change installed agent skills across sessions.

Mitigation: Review skill-sync changes before applying updates; use the documented option to skip automatic skill synchronization when appropriate.

Risk: Authentication stores a Feed Key locally.

Mitigation: Protect the local credential and manage login through the CLI rather than exposing or editing the stored key.

## Reference(s):

- [Mp2rss service](https://mp2rss.bugcode.dev)
- [Mp2rss documentation](https://areyoubugcoder.github.io/Mp2RSS/)
- [Authentication guide](references/auth.md)
- [Installation and updates](references/install.md)
- [WeChat account commands](references/mp.md)
- [X account commands](references/x.md)
- [Error handling](references/errors.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with CLI commands and content summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the mp2rss CLI and an authorized Feed Key for account operations.]

## Skill Version(s):

0.2.3 (source: frontmatter, package.json, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
