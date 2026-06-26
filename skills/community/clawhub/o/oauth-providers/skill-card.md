## Description: <br>
Adds an OAuth settings tab to the OpenClaw Control UI for connecting AI model providers through Anthropic subscription tokens, OpenAI Codex PKCE OAuth, and API keys for Anthropic, OpenAI, Google Gemini, and OpenRouter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add provider connection UI, gateway handlers, and setup guidance for OAuth, subscription-token, and API-key authentication. It also helps diagnose auth-profile ordering, stale credentials, and provider badge behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reuse Claude or OpenAI subscription credentials and stores auth profiles and secrets under ~/.openclaw, which may create account, policy, or secret-exposure risk. <br>
Mitigation: Prefer provider API keys unless subscription-credential reuse is intentional, review provider terms before use, and inspect or remove stored profiles and secrets after setup. <br>
Risk: The Anthropic auto-detect flow reads Claude CLI credentials from ~/.claude/.credentials.json. <br>
Mitigation: Use auto-detect only when the account and policy implications are understood, and verify the resulting stored profile before routing model traffic through it. <br>
Risk: Stored auth-profile order or lastGood state can select stale or unintended credentials. <br>
Mitigation: Check the OpenClaw auth profile store before use, remove stale order and lastGood entries when troubleshooting, or set an explicit provider order. <br>


## Reference(s): <br>
- [OAuth Providers ClawHub Page](https://clawhub.ai/maverick-software/oauth-providers) <br>
- [controller.ts](references/controller.ts) <br>
- [view.ts](references/view.ts) <br>
- [auth-login.ts](references/auth-login.ts) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with TypeScript reference files and JSON and bash snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes credential setup and troubleshooting guidance; provider login actions require user-controlled credentials and local OpenClaw configuration.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
