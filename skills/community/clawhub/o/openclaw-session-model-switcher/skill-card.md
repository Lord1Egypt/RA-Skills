## Description:

Instantly switch the current OpenClaw session model; supports gpt, claude, qianwen, minimax, current model status, configured model listing, and restoring the default session model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dpbs-715](https://clawhub.ai/user/dpbs-715)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to switch, reset, inspect, and list the current session model from the active OpenClaw configuration without changing global configuration or restarting the Gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates model resolution to workspace scripts and may act on returned session commands.

Mitigation: Use it only in trusted workspaces where the referenced scripts are trusted, immutable by untrusted users, and expected to return valid /model commands.

Risk: Weak validation of returned commands could cause an incorrect or unintended session model change.

Mitigation: Review helper behavior before installation and prefer a version that bundles vetted helpers or uses a scoped session-model API.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dpbs-715/skills/openclaw-session-model-switcher)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown-style text with session /model commands and readable candidate lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depends on active OpenClaw models.providers configuration and session-level model command support.]

## Skill Version(s):

0.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
