## Description:

Registers a new OmniMemory SaaS account when needed, verifies OTP, creates a first-party API key, optionally binds a third-party LLM key, then installs, configures, repairs, and verifies the @omni-pt/omnimemory-overlay plugin for OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pt-vu](https://clawhub.ai/user/pt-vu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to complete OmniMemory onboarding end to end, including account setup, API key creation, plugin installation, configuration repair, and a memory recall smoke test.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The onboarding flow can collect account credentials, OTPs, API keys, and external LLM keys in chat.

Mitigation: Use a first-party browser or OAuth-style setup where possible, avoid reused passwords, and mask or avoid sharing raw secrets after creation.

Risk: The skill sends onboarding and memory traffic to an unexplained sealoshzh.site endpoint.

Mitigation: Install only after confirming that the OmniMemory operator and endpoint are trusted for the account and data being configured.

Risk: The plugin installation command does not pin a package version.

Mitigation: Verify the @omni-pt package publisher and selected version before installation, and review the command before execution.

Risk: Automatic memory capture is enabled by default and may store future conversation content remotely.

Mitigation: Disable autoCapture unless remote memory storage is intentional and appropriate for the user's data.

## Reference(s):

- [Setup Guide](references/setup-guide.md)
- [Troubleshooting](references/troubleshooting.md)
- [ClawHub Skill Page](https://clawhub.ai/pt-vu/skills/omnimemory-full-onboarding)
- [OmniMemory](https://www.omnimemory.ai/zh/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown status summaries with explicit shell commands, API steps, warnings, and verification results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Masks secrets in summaries and reports onboarding, plugin configuration, and smoke test status.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
