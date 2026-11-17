## Description:

Fetch articles from Karpathy's curated 93 RSS feeds and generate a Chinese tech daily newsletter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mesevenjourney](https://clawhub.ai/user/mesevenjourney)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical readers, and newsletter authors use this skill to fetch recent posts from a curated RSS feed list, select high-value items, read source articles, and produce a structured Chinese technology daily brief.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to GitHub Pages, RSS feeds, and article sites.

Mitigation: Run it in a restricted workspace or network-controlled environment and review the target feed sources before use.

Risk: The workflow uses uv to run a Python script with unresolved dependency versions.

Mitigation: Pin or review dependency versions before operational use.

Risk: The remote OPML and RSS sources are mutable, so generated briefs may change as sources change.

Mitigation: Pin or archive the OPML/feed inputs when repeatability or auditability is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mesevenjourney/skills/karpathy-curated-rss-brief)
- [Newsletter output template](references/output-template.md)
- [Karpathy curated RSS OPML](https://mesevenjourney.github.io/static/hn-popular-blogs-2025.opml)
- [Karpathy RSS list post](https://x.com/karpathy/status/2018043254986703167)
- [The web is bearable with RSS](https://pluralistic.net/2026/03/07/reader-mode/)
- [uv documentation](https://docs.astral.sh/uv/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown newsletter and JSON article-fetch output during workflow execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a dated Markdown newsletter file in the current working directory and validates the generated Chinese text for Unicode replacement characters.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
