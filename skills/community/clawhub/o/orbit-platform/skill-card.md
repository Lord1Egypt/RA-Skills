## Description:

ORBIT Platform helps developers build and operate an agentic applied-intelligence platform using Node.js/TypeScript, Fastify, OpenAI Agents SDK, Supabase, Telegram, and a React dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drivercagropecuaria-cyber](https://clawhub.ai/user/drivercagropecuaria-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement and operate the ORBIT workflow: Telegram or dashboard intake, specialized research and analysis agents, Supabase persistence, dossier generation, presentation output, tracing, and quality gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill references live credential locations and broad platform setup guidance, which could lead agents to read or expose secrets.

Mitigation: Do not let agents read, echo, or persist credential files; use environment variables, secret scanning, and explicit secret-handling review before deployment.

Risk: The artifact recommends broad Supabase service role access for platform operations.

Mitigation: Replace blanket service role use with least-privilege server-side credentials, route privileged actions through trusted backend code, and review row-level security boundaries.

Risk: Telegram webhook ingestion can accept untrusted external input into the ORBIT workflow.

Mitigation: Authenticate webhook requests, validate and sanitize payloads, rate-limit ingress, and record only the minimum data required for operation.

Risk: Stored user profiles, conversation memory, research evidence, dossiers, and notifications may contain personal or sensitive data.

Mitigation: Add privacy, retention, deletion, and access-control policies before use with real users or customer data.

Risk: Generated self-contained HTML presentations may include unsafe or misleading content.

Mitigation: Escape dynamic content, sandbox previews, block external dependencies, and require quality review before publication or delivery.

## Reference(s):

- [Contratos de Dados - ORBIT](artifact/references/contratos-dados.md)
- [Perfis Completos dos Agentes - ORBIT](artifact/references/perfis-agentes.md)
- [Schema Supabase - ORBIT](artifact/references/schema-supabase.md)
- [Exemplos de Codigo - Agentes ORBIT](artifact/references/exemplos-agentes.md)
- [OpenAlex Works API](https://api.openalex.org/works?search=)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript examples, JSON data contracts, Supabase schema notes, and operational rules.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Portuguese-language operating guidance for ORBIT agents, quality gates, tracing, and generated dossier or presentation artifacts.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
