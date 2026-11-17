## Description:

Enable `openai-codex/gpt-5.4` in OpenClaw through a config-layer patch instead of rebuilding the app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youxitianguo](https://clawhub.ai/user/youxitianguo)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw power users use this skill to add and verify the `openai-codex/gpt-5.4` provider, model, alias, and fallback entries through a reversible configuration workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Changing the OpenClaw configuration can affect model routing or fallback behavior.

Mitigation: Back up `~/.openclaw/openclaw.json`, merge changes into the existing structure, and verify with `openclaw models list` and `session_status`.

Risk: The `openai-codex/gpt-5.4` route may not be appropriate for every OpenClaw environment.

Mitigation: Confirm the provider route, API settings, and authentication setup are appropriate before applying the workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/youxitianguo/skills/openclaw-codex-gpt54-enable)
- [Project Homepage](https://github.com/youxitianguo/openclaw-skill-openclaw-codex-gpt54-enable)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with shell command and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes verification and rollback steps for an OpenClaw configuration change.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
