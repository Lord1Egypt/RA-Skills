## Description:

Teach an OpenClaw agent the recommended Gmail OAuth2 setup, scope choices, and safety guardrails from this guide.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bullkis1](https://clawhub.ai/user/bullkis1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill when they want article-aligned guidance for configuring Gmail OAuth2 access, choosing scopes carefully, and identifying approval points before granting mailbox permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates a sensitive Gmail OAuth setup to a mutable external article without locally pinning the exact safe procedure or allowed scopes.

Mitigation: Review the external article and requested Gmail scopes before use, and approve only the Gmail read, modify, send, or delete permissions that are specifically needed.

Risk: OAuth client secrets, authorization codes, access tokens, refresh tokens, or mailbox contents may be exposed if shared with untrusted sites or prompts.

Mitigation: Keep OAuth secrets, tokens, authorization codes, and mailbox contents out of untrusted services and review all credential-handling steps before execution.

## Reference(s):

- [How to let my OpenClaw agent get secure Gmail access](https://howtoletmyagent.xyz/articles/how-to-let-my-openclaw-agent-get-secure-gmail-access)
- [ClawHub skill page](https://clawhub.ai/bullkis1/skills/howtoletmyagent-secure-gmail-access)
- [Publisher profile](https://clawhub.ai/user/bullkis1)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Shell commands]

**Output Format:** [Markdown with inline commands and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill should call out credential handling, destructive actions, requested Gmail scopes, and approval points before making changes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
