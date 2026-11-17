## Description:

Archives accessible WeChat public account articles by converting loaded article pages into clean Markdown and saving rendered HTML snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuhedev](https://clawhub.ai/user/liuhedev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, archivists, and knowledge workers use this skill to save WeChat public account articles they can lawfully access as local Markdown, rendered HTML snapshots, and optional local image assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can open and save arbitrary URLs even though it is framed for WeChat articles.

Mitigation: Use it only with trusted WeChat article URLs and avoid passing arbitrary or third-party supplied links.

Risk: The skill opens web pages through Playwright and writes local Markdown, HTML, and optional image snapshots.

Mitigation: Run it in an isolated environment when handling untrusted links or content, and review output before reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuhedev/skills/lh-wechat-to-markdown)

## Skill Output:

**Output Type(s):** [markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown files with YAML front matter, rendered HTML snapshots, optional local image files, and concise command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are written to a dated local directory by default, with optional image localization into an images subdirectory.]

## Skill Version(s):

1.2.1 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
