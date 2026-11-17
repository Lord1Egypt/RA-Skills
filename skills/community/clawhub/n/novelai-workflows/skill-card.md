## Description:

NovelAI creative workflows for OpenClaw covering fiction context, chapter planning, image prompting, V5/V4.5 generation, img2img, inpainting, Vibe and Director tools, cost-aware execution, bounded transient retries, and secret-safe asset records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[techotaku39](https://clawhub.ai/user/techotaku39)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to guide OpenClaw agents through NovelAI-assisted writing, chapter illustration, image editing, cost checks, and safe asset metadata recording.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured NovelAI token could be exposed if an operator places it in chat, files, command arguments, logs, or generation metadata.

Mitigation: Use a host-managed NOVELAI_TOKEN or equivalent secret reference, and keep credentials out of prompts, generated files, logs, and metadata.

Risk: NovelAI image operations and optional live API tests can consume account resources.

Mitigation: Start with tool discovery and cost estimates, show model and generation parameters before ambiguous or batch work, and require confirmation for expensive operations.

Risk: The skill relies on a third-party NovelAI Image MCP server for image operations.

Mitigation: Review and approve the MCP server before enabling it, keep the reference version pinned unless compatibility has been rechecked, and rerun smoke tests before changing the pin.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/techotaku39/skills/novelai-workflows)
- [Project homepage](https://github.com/techotaku39/openclaw-novelai)
- [NovelAI Image MCP](https://github.com/xinvxueyuan/NovelAI-Image-MCP)
- [Compatibility notes](COMPATIBILITY.md)
- [Costs and quotas](docs/COSTS-AND-QUOTAS.md)
- [Full user manual](docs/FULL-USER-MANUAL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON metadata records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local project files and secret-safe asset metadata when the agent runs the bundled helpers.]

## Skill Version(s):

0.1.3 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
