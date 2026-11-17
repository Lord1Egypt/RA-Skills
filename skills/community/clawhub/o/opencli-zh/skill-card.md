## Description:

Helps an agent use the opencli CLI to access supported websites, desktop apps, and external CLIs for browsing, searching, reading feeds, viewing notifications, and performing confirmed platform write actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poiskgit](https://clawhub.ai/user/poiskgit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to route Chinese-language browsing, search, social feed, article, history, and notification tasks through opencli when the target platform is supported. It also provides guarded workflows for troubleshooting browser-backed access and creating custom website adapters after explicit user consent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser-backed targets can touch logged-in sessions and account-scoped page data.

Mitigation: Require explicit user consent before browser-state diagnostics, logged-in page inspection, request interception, or extension changes.

Risk: Custom adapter workflows can create persistent files under ~/.opencli.

Mitigation: Explain the path and persistence impact before writing adapters, and validate any created adapter with minimal opencli commands.

Risk: Global installation of opencli may use an unpinned package version.

Mitigation: Prefer a pinned, reviewed opencli version for managed environments.

Risk: Shell command templates can become unsafe if untrusted site, URL, or goal text is interpolated directly.

Mitigation: Avoid passing untrusted values through shell command strings; quote arguments carefully and ask for confirmation before sensitive actions.

Risk: Platform write actions such as posting, replying, liking, following, deleting, subscribing, or saving can be externally visible or irreversible.

Mitigation: Confirm the target object, submitted content, and external visibility before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/poiskgit/skills/opencli-zh)
- [opencli upstream repository](https://github.com/nicepkg/opencli)
- [SKILL.md](artifact/SKILL.md)
- [Fallbacks guide](artifact/guides/fallbacks.md)
- [Custom adapters guide](artifact/guides/custom-adapters.md)
- [Custom adapters reference](artifact/guides/custom-adapters-reference.md)
- [Reference bootstrap guide](artifact/guides/reference-bootstrap.md)
- [Google reference](artifact/references/google.md)
- [Twitter / X reference](artifact/references/twitter.md)
- [Bilibili reference](artifact/references/bilibili.md)
- [Xiaohongshu reference](artifact/references/xiaohongshu.md)
- [Zhihu reference](artifact/references/zhihu.md)
- [YouTube reference](artifact/references/youtube.md)
- [Wikipedia reference](artifact/references/wikipedia.md)
- [Hacker News reference](artifact/references/hackernews.md)
- [Reddit reference](artifact/references/reddit.md)
- [Mtime reference](artifact/references/mtime.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Concise Simplified Chinese Markdown with inline shell commands and optional JSON output requests.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run opencli commands, summarize command results, and request explicit confirmation before write actions, browser-state diagnostics, or persistent adapter changes.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
