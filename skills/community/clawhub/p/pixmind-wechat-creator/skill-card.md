## Description:

Create, review, illustrate, and format WeChat Official Account articles through Pixmind's private content engine, then copy the rich article into the WeChat editor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuyunzhishang](https://clawhub.ai/user/fuyunzhishang)

### License/Terms of Use:

MIT-0

## Use Case:

External content teams and creators use this skill to plan, draft, review, optionally illustrate, and render WeChat Official Account articles for rich-text copy into the WeChat editor.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external-host fallback CLI can send the Pixmind bearer token and article materials to an API host selected through the environment.

Mitigation: Use Pixmind Builder transport when available; for CLI use, run only in a trusted environment and leave PIXMIND_API_BASE_URL unset unless the endpoint is trusted.

Risk: Article topics, source URLs, material-file contents, and generated project data are uploaded to Pixmind and may consume credits.

Mitigation: Review materials before submission, avoid sensitive content unless appropriate for Pixmind processing, and obtain explicit approval before paid generation.

## Reference(s):

- [Pixmind WeChat Creator on ClawHub](https://clawhub.ai/fuyunzhishang/skills/pixmind-wechat-creator)
- [Publisher profile](https://clawhub.ai/user/fuyunzhishang)
- [Public tool contracts](references/public-tool-contracts.md)
- [Public safety rules](references/public-safety-rules.md)
- [Article presentation](references/presentation-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Structured article presentation with rich-text HTML, Markdown fallback, JSON metadata, and optional shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports WeChat themes and layout profiles; image generation is optional and may consume Pixmind credits.]

## Skill Version(s):

0.3.6 (source: skill.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
