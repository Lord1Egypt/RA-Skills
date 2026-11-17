## Description:

High-availability multi-role model router for OpenClaw that discovers available models, maps them to role-based departments, routes tasks by complexity and domain, avoids dead auth chains, and degrades gracefully when providers fail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rexnode](https://clawhub.ai/user/rexnode)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route OpenClaw tasks across role-specific models, validate provider health, benchmark model performance, and preserve continuity through cross-provider fallback and degraded mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configurable provider endpoints and local API credentials can expose secrets or route requests to untrusted services.

Mitigation: Use only trusted provider configurations, require HTTPS for remote providers, avoid custom or plaintext baseUrl values, and limit exposed API-key environment variables.

Risk: Conversation state may be stored locally with weak path controls when session mode is used.

Mitigation: Prefer workspace-scoped installation and avoid --session for sensitive conversations until session IDs and file permissions are hardened.

Risk: The skill can execute provider API calls and update local routing state.

Mitigation: Review before installing or running, keep probe payloads minimal, and use only provider configurations you trust.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rexnode/skills/imperial-orchestrator)
- [Architecture Notes](references/ARCHITECTURE.md)
- [OpenClaw Repository](https://github.com/openclaw/openclaw)
- [Three Departments and Six Ministries Reference](https://github.com/cft0808/edict)
- [PUA Prompt Engineering Reference](https://github.com/tanweai/pua)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and JSON routing or execution state]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected model, fallback chain, role prompts, health state, token counts, cost estimates, and degraded-mode reasoning.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
