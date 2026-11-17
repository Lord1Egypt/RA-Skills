## Description:

Checks whether OpenClaw model provider configuration is complete and whether configured models can connect and return content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonzhang2015](https://clawhub.ai/user/jasonzhang2015)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to diagnose OpenClaw model provider configuration after configuration changes or when a user asks to test models. It can help identify missing settings, unreachable endpoints, invalid API keys, and models that do not return content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist API keys in OpenClaw model configuration and use them in real provider API calls.

Mitigation: Use keys only with trusted provider endpoints and rotate any key that may have been tested against an untrusted baseUrl.

Risk: The skill can make automatic network requests to configured model provider URLs during diagnostics.

Mitigation: Prefer HTTPS-only provider URLs, avoid untrusted custom relays, and review the configured baseUrl before running checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jasonzhang2015/skills/model-config-check)
- [Skill instructions](artifact/SKILL.md)
- [Model check script](artifact/scripts/check_models.sh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-style diagnostic report with provider status, model test results, and troubleshooting advice]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke network connectivity checks and provider API calls using configured model credentials.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
