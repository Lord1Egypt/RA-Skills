## Description:

Transforms podcast transcripts, episode links, notes, or summaries into structured publish-ready articles with formats for Markdown, WeChat, Zhihu, newsletters, and standalone HTML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijinhongucl-pixel](https://clawhub.ai/user/lijinhongucl-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketing teams, and internal communications teams use this skill to turn podcast material into readable Chinese articles, summaries, reconstructed interviews, social media slices, or HTML pages for publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated webpage output may carry unsafe active content from untrusted podcast material into a browser page.

Mitigation: Escape plain-text fields, sanitize BODY and QUOTES, and review generated HTML for scripts, event handlers, dangerous links, iframes, forms, SVG/MathML, and other active content before opening or publishing it.

## Reference(s):

- [Output Style Templates](artifact/references/styles.md)
- [Platform Formatting Guidelines](artifact/references/platforms.md)
- [Quote Extraction Rules](artifact/references/quote-extraction.md)
- [ClawHub Skill Page](https://clawhub.ai/lijinhongucl-pixel/skills/podcast-article)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Guidance]

**Output Format:** [Markdown article, platform-specific plain text, or standalone HTML]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save outputs as article.md or article.html in a dated task folder; webpage mode uses the bundled HTML template.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
