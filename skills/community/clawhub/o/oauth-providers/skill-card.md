## Description:

Adds an "OAuth" settings tab to the OpenClaw Control UI for connecting AI model providers with Anthropic subscription tokens, OpenAI Codex PKCE OAuth, API keys, auth-profile troubleshooting, badge rendering references, and encrypted credential storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to add and troubleshoot OpenClaw provider authentication through OAuth, subscription-token, and API-key flows for Anthropic, OpenAI, Google Gemini, and OpenRouter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles high-value provider credentials, including OAuth tokens, subscription tokens, and API keys.

Mitigation: Review the skill before installing, prefer manual token or API-key paths, and confirm credential storage and handling meet local security requirements.

Risk: The Anthropic auto-detect flow reads Claude CLI credentials and can copy a Claude CLI token into OpenClaw storage.

Mitigation: Use the auto-detect flow only with explicit informed consent, or disable it and require users to paste a token or API key manually.

Risk: Raw token material may be returned through UI-facing RPC responses during auto-detection.

Mitigation: Avoid returning raw tokens to the browser and return only status, masked identifiers, or profile metadata.

Risk: Subscription-token use may carry provider policy risk outside the provider's intended client.

Mitigation: Confirm provider terms and switch to a supported API-key path when authorization errors or policy restrictions apply.

Risk: OAuth sessions are tracked in process memory and should be isolated from unrelated users or browser sessions.

Mitigation: Use stronger OAuth session isolation, short session lifetimes, and explicit session binding before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maverick-software/skills/oauth-providers)
- [SKILL.md](SKILL.md)
- [auth-login.ts](references/auth-login.ts)
- [controller.ts](references/controller.ts)
- [view.ts](references/view.ts)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript source files and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes UI, controller, and gateway handler source files plus setup and troubleshooting steps.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
