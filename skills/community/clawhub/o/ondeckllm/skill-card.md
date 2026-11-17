## Description:

OnDeckLLM provides a localhost dashboard for managing LLM providers, model routing, fallback chains, provider health, latency, and optional OpenClaw configuration discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[canonflip-git](https://clawhub.ai/user/canonflip-git)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to check, open, and operate a local OnDeckLLM dashboard for managing LLM provider configuration, model routing priority, fallback chains, health checks, latency, and cost tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to globally install and run an unpinned third-party npm package.

Mitigation: Prefer a pinned, audited OnDeckLLM version and avoid running the global install with elevated privileges.

Risk: The dashboard can read and modify local OpenClaw provider configuration.

Mitigation: Back up ~/.openclaw/openclaw.json before using the dashboard and review provider changes before syncing them.

Risk: OnDeckLLM stores local provider settings and usage records under ~/.ondeckllm/.

Mitigation: Review the contents and permissions of ~/.ondeckllm/, including usage.jsonl, according to local privacy and retention expectations.

## Reference(s):

- [OnDeckLLM website](https://ondeckllm.com)
- [OnDeckLLM npm package](https://www.npmjs.com/package/ondeckllm)
- [OnDeckLLM GitHub Issues](https://github.com/canonflip/ondeckllm/issues)
- [ClawHub skill page](https://clawhub.ai/canonflip-git/skills/ondeckllm)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The status helper emits running, port, url, pid, and HTTP status when available.]

## Skill Version(s):

1.4.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
