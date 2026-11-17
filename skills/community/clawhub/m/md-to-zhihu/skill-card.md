## Description:

Converts Markdown articles to Zhihu publishing format and supports preview, draft, and one-click publishing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejianjun000](https://clawhub.ai/user/xiejianjun000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content publishers use this skill to convert Markdown into Zhihu-compatible HTML previews or content and optionally automate drafting or publishing articles to Zhihu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable Zhihu login cookies and browser profile data may be stored in the skill directory.

Mitigation: Keep the skill directory private and do not commit, share, or publish generated .zhihu_cookies.json or .zhihu_browser_profile data.

Risk: Authenticated automation can create drafts or publish articles to Zhihu.

Mitigation: Use draft mode first, review the article in Zhihu, and confirm the target account and topics before publishing.

Risk: Markdown from untrusted sources may be previewed or published as converted HTML.

Mitigation: Sanitize and review untrusted Markdown before conversion, preview, or publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejianjun000/skills/md-to-zhihu)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands; generated HTML files and Zhihu draft or article URLs when publishing succeeds]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write HTML preview/content files and can control an authenticated Zhihu publishing session using stored login cookies.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
