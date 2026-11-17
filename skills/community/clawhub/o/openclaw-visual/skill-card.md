## Description:

OpenClaw Visual helps agents turn OpenClaw content such as PhoenixClaw journals, chat logs, individual messages, summaries, and long-form text into shareable, locally rendered images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goforu](https://clawhub.ai/user/goforu)

### License/Terms of Use:

MIT

## Use Case:

External OpenClaw users and developers use this skill to convert personal notes, PhoenixClaw journals, chat records, quotes, photos, summaries, and article-style content into formatted PNG images for chat or social sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process private journals, chat logs, and summaries.

Mitigation: Use only the specific local files needed for the requested image, redact sensitive content before rendering, and preview generated images before sharing them.

Risk: Rendering untrusted HTML or attacker-provided image URLs in a browser path could expose sensitive content or local network resources.

Mitigation: Avoid untrusted HTML and unknown image URLs, run rendering in an isolated environment with no sensitive local network access, and pin or update browser-rendering dependencies before routine use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/goforu/skills/openclaw-visual)
- [Template design specifications](references/templates.md)
- [Content parsing rules](references/content-parsing.md)
- [Local image rendering setup](references/rendering-setup.md)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Guidance]

**Output Format:** [PNG image files and JSON status, with Markdown guidance and shell command examples when invoked by an agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local HTML/CSS templates with node-html-to-image by default and Playwright when advanced rendering is requested.]

## Skill Version(s):

0.0.1 (source: SKILL.md metadata, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
