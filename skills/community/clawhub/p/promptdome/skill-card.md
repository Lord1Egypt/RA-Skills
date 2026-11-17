## Description:

Integrate PromptDome prompt injection screening into OpenClaw by installing a hook that scans incoming messages and an agent tool that can scan untrusted content on demand.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tschew72](https://clawhub.ai/user/tschew72)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to add prompt-injection screening for incoming messages and to let agents explicitly scan web content, files, tool outputs, or other untrusted text before processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incoming message text is automatically sent to PromptDome or a configured endpoint, which can expose secrets, customer data, private messages, or regulated content.

Mitigation: Use a self-hosted or tightly allowlisted endpoint and restrict where the hook is enabled.

Risk: The skill stores an API key in OpenClaw configuration and writes scan logs that include message previews.

Mitigation: Harden OpenClaw config and log permissions, review log retention, and rotate the API key if exposure is suspected.

Risk: The hook fails open when the PromptDome API is unreachable or returns an error, so messages may pass without a warning.

Mitigation: Monitor scan failures and use additional controls in environments that require blocking behavior.

Risk: Security guidance flags installer heredoc and warning-field sanitization issues before production use.

Mitigation: Fix those issues and re-scan the release before deploying it in production.

## Reference(s):

- [PromptDome documentation](https://promptdome.cyberforge.one/docs)
- [PromptDome API key dashboard](https://promptdome.cyberforge.one/dashboard/api-keys)
- [PromptDome shield API endpoint](https://promptdome.cyberforge.one/api/v1/shield)
- [PromptDome ClawHub skill page](https://clawhub.ai/tschew72/skills/promptdome)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and text or JSON scan results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PROMPTDOME_API_KEY; scan requests send up to 50,000 characters to PromptDome or a configured endpoint.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
