## Description:

Set up AI-powered Gmail monitoring in OpenClaw that watches an inbox via Google Pub/Sub, classifies email with an LLM, and forwards important messages to Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nanaco666](https://clawhub.ai/user/nanaco666)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to install and configure a Gmail-to-Telegram monitoring workflow in OpenClaw, including Google Cloud Pub/Sub setup, plugin configuration, testing, troubleshooting, reconfiguration, and uninstall steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private Gmail metadata and snippets may be forwarded to Telegram and, when llmApiKey is configured, to the selected LLM provider.

Mitigation: Confirm this data flow before installation, choose Telegram recipients deliberately, and use only a trusted LLM endpoint.

Risk: The LLM API key is stored in OpenClaw plugin configuration.

Mitigation: Secure OpenClaw plugin configuration and use a scoped or replaceable API key.

Risk: The setup flow installs a remote GitHub archive.

Mitigation: Verify the downloaded plugin source or digest before following the archive install command.

Risk: Gmail and Pub/Sub setup can expose inbox events beyond the user's intent if configured broadly.

Mitigation: Use a dedicated low-privilege Google Cloud project and review Gmail API, Pub/Sub topic, and subscription permissions before enabling the watch.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nanaco666/skills/openclaw-mail-agent)
- [Mail Agent homepage from skill metadata](https://github.com/nanaco666/openclaw-mail-agent)
- [OpenClaw](https://openclaw.ai)
- [gog Gmail CLI](https://gogcli.sh)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup, testing, troubleshooting, reconfiguration, and uninstall guidance for an OpenClaw plugin.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
