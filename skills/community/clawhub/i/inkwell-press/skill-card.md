## Description:

Helps turn Markdown into WeChat-ready HTML, magazine-style covers, and Xiaohongshu social cards, with optional clipboard or WeChat draft publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijinhongucl-pixel](https://clawhub.ai/user/lijinhongucl-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and publishing teams use this skill to format articles for WeChat, create covers and social cards, check content, and optionally send finished drafts to the clipboard or a WeChat account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing or CDN image uploads can expose article content or images to WeChat, GitHub, or jsDelivr.

Mitigation: Explain the destination and obtain user confirmation before publishing or enabling uploads; provide credentials only for requested features.

Risk: External images in Markdown are downloaded by default, including in private or offline workflows.

Mitigation: Use --no-embed-external for sensitive, offline, intranet, or untrusted Markdown.

Risk: Clipboard publishing replaces existing clipboard contents and may expose a draft if pasted elsewhere.

Mitigation: Confirm clipboard publishing with the user and check the intended paste destination.

Risk: Installing unreviewed dependencies can introduce supply-chain risk.

Mitigation: Install in an isolated virtual environment and prefer the hash-checked requirements file.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/lijinhongucl-pixel/skills/inkwell-press)
- [Project homepage](https://github.com/lijinhongucl-pixel/inkwell)
- [Supply chain and installation guidance](artifact/SUPPLY_CHAIN.md)

## Skill Output:

**Output Type(s):** [HTML, Images, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance and CLI commands; generated HTML and cover or social-card images]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional clipboard output or WeChat draft publishing requires user confirmation.]

## Skill Version(s):

1.0.5 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
