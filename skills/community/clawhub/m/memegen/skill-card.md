## Description:

Generate meme images using the memegen.link API, with guidance for choosing meme templates, formatting captions, and producing meme URLs or downloaded image files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[artemiopadilla](https://clawhub.ai/user/artemiopadilla)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use Memegen to teach an agent to choose meme templates, format captions, and create meme image URLs or downloaded image files for user-requested memes and reaction images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional scripts and examples contact third-party services and may write image files locally.

Mitigation: Run only the needed optional scripts, review their network destinations and output paths, and use a constrained working directory for production agents.

Risk: Security evidence reports unsafe command/code injection paths in optional JavaScript and Giphy examples.

Mitigation: Harden or skip those examples for untrusted input; avoid shell interpolation and validate template, caption, URL, and output path values.

Risk: The Reddit OAuth script handles raw Reddit passwords.

Mitigation: Avoid the Reddit OAuth script unless it is rewritten to use safer authentication and secret handling.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/artemiopadilla/skills/memegen)
- [memegen.link API](https://api.memegen.link)
- [memegen.link API Reference](references/api.md)
- [Template Quick-Reference Index](references/template-index.md)
- [Complete Template Catalog](references/templates-complete.md)
- [Classic Template Fallbacks](references/templates-classic.md)
- [Trending Template Sources](references/templates-trending.md)
- [Humor Profiles](humor-profiles.md)
- [Generic Integration Guide](integrations/generic.md)
- [LangChain Integration Guide](integrations/langchain.md)
- [OpenClaw Integration Guide](integrations/openclaw.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with URLs, code snippets, shell commands, and optional downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Core meme generation uses memegen.link without an API key; optional integrations may call Imgflip, Reddit, or Giphy and may write local image files.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
