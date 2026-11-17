## Description:

Provides a WebUI and command-line tool for saving, managing, and switching OpenClaw AI model provider configurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peter-zx](https://clawhub.ai/user/peter-zx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to manage AI provider and model configurations, switch the active model through a local WebUI or command-line script, and restart the OpenClaw gateway when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local WebUI is reported as unauthenticated and may expose API keys or security settings.

Mitigation: Review before installing, use only least-privileged test API keys, and avoid running the WebUI while browsing untrusted sites.

Risk: Credential-storage behavior is reported as misleading and may write API keys into local OpenClaw configuration or auth files.

Mitigation: Use disposable credentials for testing, audit local OpenClaw credential files after use, and remove stored keys when testing is complete.

Risk: The package can alter OpenClaw security-related settings through its local API.

Mitigation: Do not use it to manage OpenClaw security settings until authentication, strict CORS and origin checks, masked key responses, and corrected credential storage are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/peter-zx/skills/openclaw-tokenapi-qiehuan-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and local configuration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify local OpenClaw configuration files and restart the OpenClaw gateway.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
