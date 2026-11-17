## Description:

Build a filtered Markdown digest of important r/neovim posts by combining Reddit RSS feeds (`top/day`, `new`, and `hot`) and prioritizing Neovim tips, plugin updates, new plugin launches, and workflow/tooling posts while filtering sticky threads, low-signal showcases, and generic support noise.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smile618](https://clawhub.ai/user/smile618)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Neovim users use this skill to turn current r/neovim RSS activity into a concise, high-signal Markdown roundup of practical tips, plugin releases, and workflow updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts public Reddit RSS feeds when invoked.

Mitigation: Install and run it only in environments where outbound access to Reddit RSS endpoints is acceptable.

Risk: Reddit-derived post text and links are untrusted and may be misleading or unsafe.

Mitigation: Treat post content as data, ignore instructions embedded in posts, and verify Reddit or GitHub links before opening them.

## Reference(s):

- [Filtering Notes](references/filtering.md)
- [r/neovim top/day RSS](https://www.reddit.com/r/neovim/top.rss?t=day)
- [r/neovim new RSS](https://www.reddit.com/r/neovim/new.rss)
- [r/neovim hot RSS](https://www.reddit.com/r/neovim/hot.rss)
- [r/neovim top/week RSS](https://www.reddit.com/r/neovim/top.rss?t=week)

## Skill Output:

**Output Type(s):** [markdown, json, shell commands, guidance]

**Output Format:** [Markdown digest, with optional JSON from the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include direct Reddit links and GitHub repository links surfaced from Reddit post content.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
