## Description:

Lunara Voice lets OpenClaw agents manage Lunara Voice AI agents, campaigns, outbound calls, call history, transcripts, analytics, webhooks, tags, and LLM data export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lunara9897-jpg](https://clawhub.ai/user/lunara9897-jpg)

### License/Terms of Use:

MIT

## Use Case:

Developers and business operators use this skill to connect OpenClaw agents to Lunara Voice for real phone-call workflows, including agent management, outbound campaigns, call review, analytics, webhook management, and data export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place outbound calls and start campaigns through the configured Lunara account.

Mitigation: Require clear human approval and scoped instructions before enabling call placement or campaign starts, and verify agent minute balance and target lists before execution.

Risk: The skill can read and export call transcripts and analytics that may contain sensitive personal or business information.

Mitigation: Keep PII masking enabled where available, avoid regulated or sensitive call data unless explicitly approved, and use a test or least-privilege API key.

Risk: The skill can create, revoke, or delete API keys and create or change webhooks for the configured account.

Mitigation: Protect the local OpenClaw configuration file, use only a trusted HTTPS Lunara API URL, and restrict key and webhook management to trusted operators.

## Reference(s):

- [LunaraVox homepage](https://lunaravox.com)
- [ClawHub skill page](https://clawhub.ai/lunara9897-jpg/skills/lunara-voice)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown text with JSON API responses and inline shell or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return call transcripts, analytics summaries, export payloads, API key creation output, and webhook status.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; plugin manifests report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
