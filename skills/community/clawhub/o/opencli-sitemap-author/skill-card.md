## Description:

Use when creating or maintaining OpenCLI site sitemaps: agent-facing navigation, page-state, action, workflow, API-reference, pitfall, and fallback knowledge for a website.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaoyang78](https://clawhub.ai/user/chaoyang78)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create and maintain compact OpenCLI browser sitemaps that record durable navigation paths, actions, workflows, API references, pitfalls, and recovery guidance for websites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated sitemap or trace-derived notes may capture private data from logged-in sites.

Mitigation: Review generated sitemap and trace-derived content before promotion; remove secrets, cookies, private identifiers, private messages, and account-specific values.

Risk: Stored site navigation knowledge can become stale or conflict with the current browser state.

Mitigation: Treat current browser state as authoritative, verify paths before relying on them, and mark conflicting sitemap entries as stale instead of promoting them as facts.

Risk: Some guidance is Chinese-only, which may make review harder for teams that do not read Chinese.

Mitigation: Have a Chinese-reading reviewer check those sections or translate them before operational use.

## Reference(s):

- [Sitemap Schema Reference](references/sitemap-schema.md)
- [ClawHub Skill Page](https://clawhub.ai/chaoyang78/skills/opencli-sitemap-author)
- [ClawHub Publisher Profile](https://clawhub.ai/user/chaoyang78)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with compact YAML snippets and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents toward local overlay and reviewed global sitemap files; no hidden code or install-time behavior was reported.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
