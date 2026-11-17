## Description:

Install, configure, verify, or troubleshoot the @jwongart/openclaw-minimax-media OpenClaw plugin for MiniMax image understanding, image generation, music generation, video generation, text-to-speech, and web search tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junwongpp](https://clawhub.ai/user/junwongpp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install, configure, update, verify, migrate, and troubleshoot the MiniMax media plugin and its image, music, video, text-to-speech, and web search tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unversioned npm package can change the trusted code over time.

Mitigation: Prefer the specific-version install command and verify the npm package and GitHub source before installation.

Risk: MiniMax API keys or tokens could be exposed if committed to project files.

Mitigation: Keep real API keys out of committed files and use the documented environment variables or local OpenClaw configuration.

Risk: Enabled plugin tools may send relevant prompts or media requests to MiniMax-backed services.

Mitigation: Review the plugin behavior and only enable it in environments where those external service calls are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/junwongpp/skills/minimax-media-plugin)
- [openclaw-minimax-media GitHub repository](https://github.com/jwong-art/openclaw-minimax-media)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides installation, configuration, verification, migration, and troubleshooting guidance for an OpenClaw plugin.]

## Skill Version(s):

0.8.8 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
