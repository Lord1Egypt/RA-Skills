## Description:

Run LLM Signal GEO analyst workflows from OpenClaw to fetch deterministic GEO action plans, check site health status, and execute or review hosted or self-hosted agent workflows with approval-safe guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[immythz](https://clawhub.ai/user/immythz)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run LLM Signal GEO workflows from OpenClaw, fetch action plans, check site status, and prepare exact implementation steps for review or execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote workflow plans can trigger automatic handling of auto_safe actions.

Mitigation: Treat auto_safe actions as recommendations unless the runtime adds approval gates and allowlist controls.

Risk: The API key is sent to a configurable LLM Signal endpoint.

Mitigation: Use only trusted HTTPS endpoints, avoid untrusted LLMSIGNAL_BASE_URL values, and rotate the key if it may have been used with an untrusted endpoint.

## Reference(s):

- [LLM Signal Agent Documentation](https://www.llmsignal.app/docs/agents)
- [ClawHub Skill Page](https://clawhub.ai/immythz/skills/llm-signal-geo-analyst)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured action recommendations and optional command or diff scaffolds]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommended actions include title, priority, reason, exact steps, optional command or diff scaffold, and approval requirement.]

## Skill Version(s):

0.1.0 (source: manifest.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
