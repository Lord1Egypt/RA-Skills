## Description:

Research competitors, analyze top-ranking content, and generate a fully SEO-optimized 2000+ word blog post with headings, FAQ, meta description, and internal linking suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dreamsarts](https://clawhub.ai/user/dreamsarts)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and content teams use this skill to research search results for a target keyword and generate a publication-ready SEO blog article in Markdown. It supports CLI and Python workflows with optional brand, location, tone, target word count, and research controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A hard-coded local .env path can cause unexpected secret loading behavior or installation failures.

Mitigation: Remove or change the hard-coded .env path and provide GEMINI_API_KEY explicitly in a dedicated project environment.

Risk: The research phase connects to Chrome on localhost with an authenticated browser session.

Mitigation: Use an isolated Chrome profile for remote debugging and avoid running the skill against a personal browsing session.

Risk: Generated SEO articles may contain inaccurate, outdated, or unsuitable claims.

Mitigation: Review generated articles for factual accuracy, originality, brand fit, and publication readiness before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dreamsarts/skills/openclaw-seo-content-engine)
- [Publisher profile](https://clawhub.ai/user/dreamsarts)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown article with YAML frontmatter, headings, FAQ, meta description, and internal link suggestions; output may be printed to stdout or saved to a file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated articles should be manually reviewed before publication; default target length is 2000+ words and the generator uses a maximum Gemini response size of 8192 tokens.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
