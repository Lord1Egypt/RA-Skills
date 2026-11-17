## Description:

Convert GitHub repositories into RedNote (小红书) style technical articles, including project introductions, reviews, tutorials, tool lists, and release notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caoyachao](https://clawhub.ai/user/caoyachao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical content creators use this skill to turn GitHub repository information into Chinese RedNote-ready promotional, tutorial, review, list, or release-note content. It can also generate a platform-sized cover image when file output is requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated GitHub repository data may be cached locally by default.

Mitigation: Use a least-privilege GitHub token, avoid private repositories unless caching is disabled or isolated, and clear the local cache when repository data should not persist.

Risk: Cover-image generation has unsafe SVG handling for untrusted or unusual GitHub URLs.

Mitigation: Avoid using --with-image on untrusted inputs until SVG escaping is fixed; review generated SVG/PNG artifacts before publication.

## Reference(s):

- [Prompt Templates](references/prompts.md)
- [RedNote Style Guide](references/rednote-style.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [RedNote-style Chinese Markdown articles and optional PNG/SVG cover image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports intro, review, tutorial, list, and release templates; optional file output, clipboard copy, cache disabling, and cover image generation.]

## Skill Version(s):

1.6.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
