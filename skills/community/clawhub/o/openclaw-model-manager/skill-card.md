## Description:

Model Manager helps OpenClaw users add, remove, update, inspect, switch, and test model and provider configuration in openclaw.json.

This skill is ready for commercial/non-commercial use.

## Publisher:

[the2015](https://clawhub.ai/user/the2015)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to maintain OpenClaw model and provider settings, including adding models, updating model parameters, changing the primary model, checking availability, and troubleshooting provider errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The status-check feature can send stored API keys to every configured provider, including an opaque third-party endpoint.

Mitigation: Review provider base URLs before testing, remove unknown custom endpoints, use low-scope test keys where possible, and avoid testing all models at once unless those authenticated requests are intended.

Risk: Configuration changes can disrupt model routing if provider entries, model IDs, or JSON syntax are incorrect.

Mitigation: Review generated configuration changes before applying them and restart the OpenClaw gateway only after the intended model and provider settings are confirmed.

## Reference(s):

- [Model information reference](references/model-info.md)
- [ClawHub skill page](https://clawhub.ai/the2015/skills/openclaw-model-manager)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, text, and PowerShell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose OpenClaw configuration edits, gateway restart commands, and model connection status summaries.]

## Skill Version(s):

1.0.1 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
