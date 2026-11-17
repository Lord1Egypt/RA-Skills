## Description:

When the user wants to design, optimize, or audit masonry (Pinterest-style) layouts for content display.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kostja94](https://clawhub.ai/user/kostja94)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to choose, implement, optimize, or audit masonry layouts for galleries, portfolios, discovery feeds, and image-heavy pages with varied item heights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated masonry implementations can harm accessibility if visual order differs from logical DOM or screen reader order.

Mitigation: Review generated layout code for logical DOM order and keyboard and screen reader behavior before deployment.

Risk: Masonry galleries using infinite scroll or lazy loading can make SEO-critical content difficult for crawlers to discover.

Mitigation: Use crawlable pagination, reachable links, and search-friendly lazy-loading patterns for content that must be indexed.

Risk: Image-heavy masonry pages can introduce performance issues.

Mitigation: Review generated implementations for image sizing, lazy loading, layout stability, and page performance before release.

## Reference(s):

- [Google Search Central: Infinite scroll search-friendly recommendations](https://developers.google.com/search/blog/2014/02/infinite-scroll-search-friendly)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown prose with tables and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no code execution, persistence, or sensitive access.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
