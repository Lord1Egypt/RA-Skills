## Description:

Universal LLM gateway that routes AI coding requests across 12+ providers with complexity analysis, Graphify code intelligence, Distill compression, routing telemetry, Code Mode, and cost optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vishalveerareddy123](https://clawhub.ai/user/vishalveerareddy123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to configure Lynkr as an OpenAI-compatible routing proxy for coding agents such as Claude Code, Cursor, Codex, and OpenClaw. It helps route requests by task complexity, provider health, and cost while exposing configuration, telemetry, and admin controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles coding prompts and provider access, and server security evidence flags under-scoped install and local data exposure controls.

Mitigation: Review the upstream package and installer before installing; prefer a pinned version, isolated environment or dedicated user account, localhost-only binding, endpoint authentication, and a clear purge path for telemetry, prompt cache, and long-term memory.

Risk: Routing coding prompts through local and cloud providers may expose sensitive code, credentials, or project context if the proxy or provider configuration is mis-scoped.

Mitigation: Route only approved data through configured providers, keep provider credentials isolated, and disable or clear telemetry, prompt cache, and memory before handling sensitive repositories.

## Reference(s):

- [Lynkr GitHub repository](https://github.com/Fast-Editor/Lynkr)
- [ClawHub skill page](https://clawhub.ai/vishalveerareddy123/skills/lynkr)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, env, and JSON configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include localhost proxy endpoint, provider routing tiers, telemetry endpoints, and admin endpoint guidance.]

## Skill Version(s):

8.0.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
