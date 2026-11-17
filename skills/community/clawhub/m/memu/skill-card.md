## Description:

Persistent memory infrastructure for 24/7 agents that packages memU integration guidance, examples, and configuration for long-term context retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[projectsnowwork](https://clawhub.ai/user/projectsnowwork)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent engineers use this skill to integrate memU as a long-term memory layer for always-on agents that need persistent context, scoped retrieval, and examples for OpenClaw or generic agent loops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-term memory can retain sensitive user or customer data beyond the current session.

Mitigation: Collect explicit consent, redact sensitive inputs, and define retention and deletion controls before storing personal, regulated, email, log, or customer data.

Risk: Example PostgreSQL setup uses default credentials and a public port binding.

Mitigation: Use non-default credentials, restrict network exposure, and run databases in isolated environments with pinned dependencies.

Risk: Retrieved memory can be stale, poisoned, or scoped to the wrong user or tenant.

Mitigation: Scope every memorize and retrieve call by user or tenant, enforce tenant isolation, and treat retrieved memory as untrusted reference data rather than system instructions.

Risk: The examples require API credentials for LLM and embedding calls.

Mitigation: Use scoped environment variables, rotate keys regularly, and avoid writing secrets into prompts, memory payloads, logs, or shared configuration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/projectsnowwork/skills/memu)
- [memU Repository](https://github.com/NevaMind-AI/memU)
- [memU English Documentation](https://github.com/NevaMind-AI/memU/blob/main/readme/README_en.md)
- [memU Benchmark Results](https://memu.pro/benchmark)
- [memU Cloud API](https://api.memu.so)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples require python3 and OPENAI_API_KEY; persistent deployments may use PostgreSQL with pgvector.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
