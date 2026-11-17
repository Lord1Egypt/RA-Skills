## Description:

Create high-quality visual designs, including websites, app screens, dashboards, slides, marketing materials, social media graphics, UI designs, mockups, wireframes, layouts, webpages, app screens, presentation slides, posters, banners, and marketing assets using the Pencil CLI tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gerhardberger](https://clawhub.ai/user/gerhardberger)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and agents use this skill to generate and iterate on visual design artifacts from natural language prompts through the Pencil CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill normalizes running mutable npm or CDN content and replacing persistent agent skill instructions without strong pinning, integrity checks, or consent gates.

Mitigation: Use a pinned, project-local @pencil.dev/cli version, verify downloaded SKILL.md contents before activation, and avoid overwriting persistent agent skill directories from @latest CDN URLs.

Risk: The skill can send design prompts and selected design files to external Pencil and Claude-backed AI processing.

Mitigation: Install and run it only when external AI processing is acceptable for the prompts and files involved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gerhardberger/skills/pencil-design)
- [OpenClaw skills documentation](https://docs.openclaw.ai/skills/)
- [Pencil CLI SKILL.md on unpkg](https://unpkg.com/@pencil.dev/cli@latest/SKILL.md)
- [Pencil CLI SKILL.md on jsDelivr](https://cdn.jsdelivr.net/npm/@pencil.dev/cli@latest/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to create .pen design files and exported image files when the Pencil CLI is available and authenticated.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
