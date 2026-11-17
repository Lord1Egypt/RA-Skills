## Description:

Manage and configure the Kiwi Voice assistant service for start and stop workflows, voice configuration, logs, audio troubleshooting, and voice profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuangu260](https://clawhub.ai/user/yuangu260)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run, configure, and troubleshoot a self-hosted Kiwi Voice assistant connected to OpenClaw. It helps manage speech-to-text, text-to-speech, audio device, security approval, and voice profile settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary reports unsafe defaults and broad admin control that require review before installation.

Mitigation: Review the package before deployment, reduce OpenClaw scopes below operator.admin, and replace unsafe defaults with least-privilege settings.

Risk: The release security guidance flags exposed APIs, committed token material, permissive approval behavior, and remote audio URL fetching as areas needing attention.

Mitigation: Bind APIs to localhost or a private network, replace any committed token with a unique secret, enable authentication, disable Telegram auto-approve fallback, and restrict remote audio URL fetching in RunPod deployments.

Risk: The release security guidance calls out never-refuse system prompts that may increase misuse risk.

Mitigation: Remove or rewrite never-refuse prompts before production use and require review for sensitive actions.

## Reference(s):

- [Kiwi Voice ClawHub release](https://clawhub.ai/yuangu260/skills/kiwi-voice)
- [Kiwi Voice documentation](https://docs.kiwi-voice.com)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [Kiwi Voice website](https://kiwi-voice.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local configuration files, logs, service commands, and voice profile files.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
