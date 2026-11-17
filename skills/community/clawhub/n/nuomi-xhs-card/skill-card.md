## Description:

Converts local Markdown or MDX content into Xiaohongshu-style PNG card images using built-in templates, light/dark modes, and pagination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangyijun](https://clawhub.ai/user/tangyijun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and content operators use this skill to guide an agent through choosing a template and running a local CLI that renders Markdown/MDX posts into paginated social card PNGs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rendering untrusted Markdown, MDX, or raw HTML may execute active content or preserve unsafe markup.

Mitigation: Render only trusted content by default; avoid MDX mode and raw HTML from other people unless the renderer is sandboxed.

Risk: Remote image processing can make network requests while rendering content.

Mitigation: Disable remote-image processing for untrusted documents or run it in an environment with contained network egress.

Risk: Pinned dependencies may become stale before CI or sensitive-project use.

Mitigation: Update and rescan dependencies before using the renderer in CI or on sensitive projects.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tangyijun/skills/nuomi-xhs-card)
- [CLI Reference](artifact/references/cli-reference.md)
- [Template Reference](artifact/references/templates.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files, Configuration]

**Output Format:** [Markdown guidance with inline shell commands; the CLI produces PNG card files and optional JSON render reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports theme, mode, split strategy, size, scale, pager, output directory, maximum pages, MDX mode, and debug output options.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
