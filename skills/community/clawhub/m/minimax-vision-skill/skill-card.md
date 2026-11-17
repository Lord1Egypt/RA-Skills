## Description:

MiniMax Vision Skill helps agents analyze images through the MiniMax mmx CLI for local files or image URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gawainchin](https://clawhub.ai/user/gawainchin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route explicit MiniMax vision requests through the MiniMax CLI for image understanding of local files or URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing a global CLI package can introduce supply-chain or privilege risk.

Mitigation: Install mmx-cli only from a trusted npm source, avoid sudo, and consider pinning a reviewed version.

Risk: MiniMax API keys can be exposed through shared terminals, logs, scripts, or source control.

Mitigation: Enter keys only in trusted environments, keep them out of logs and repositories, and rotate any key that may have been exposed.

Risk: Image analysis sends local files or image URLs to the MiniMax CLI service flow.

Mitigation: Use the skill only with images the user is authorized to process and avoid submitting sensitive content unless approved for that service.

## Reference(s):

- [MiniMax API key page](https://platform.minimax.io/user-center/basic-information/interface-key)
- [ClawHub skill page](https://clawhub.ai/gawainchin/skills/minimax-vision-skill)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local mmx-cli installation and MiniMax API authentication.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
