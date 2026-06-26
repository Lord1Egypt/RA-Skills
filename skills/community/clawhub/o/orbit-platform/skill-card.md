## Description: <br>
ORBIT Platform guides developers in building and operating an agentic intelligence platform with a Node.js/TypeScript backend, OpenAI Agents SDK agents, Supabase storage, Telegram intake, and a React dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drivercagropecuaria-cyber](https://clawhub.ai/user/drivercagropecuaria-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to implement or extend the ORBIT platform, including specialized research, analysis, dossier, presentation, and quality-review agents. It also guides Supabase schema usage, Telegram webhook integration, React dashboard work, queue processing, tracing, migrations, and quality gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill normalizes broad Supabase admin credentials and service_role-style access. <br>
Mitigation: Replace broad defaults with least-privilege keys and scoped database policies before deployment. <br>
Risk: The artifact points agents toward local credential-file access. <br>
Mitigation: Inject secrets through managed secret stores or environment variables and prevent agents from reading credential files directly. <br>
Risk: Telegram messages and user profile data may contain personal or sensitive information. <br>
Mitigation: Define privacy, retention, and deletion rules before storing Telegram content or user profile records. <br>
Risk: Generated dossiers, analyses, and presentations may contain incorrect or misleading claims. <br>
Mitigation: Require the documented quality gates, source review, and human approval before user-facing delivery. <br>


## Reference(s): <br>
- [Contratos de Dados - ORBIT](references/contratos-dados.md) <br>
- [Perfis Completos dos Agentes - ORBIT](references/perfis-agentes.md) <br>
- [Schema Supabase - ORBIT](references/schema-supabase.md) <br>
- [Exemplos de Codigo - Agentes ORBIT](references/exemplos-agentes.md) <br>
- [OpenAlex Works API](https://api.openalex.org/works?search=) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with TypeScript, SQL, JSON, and command-oriented implementation details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Portuguese-language project guidance for ORBIT implementation and operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
