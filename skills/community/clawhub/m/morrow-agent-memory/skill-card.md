## Description: <br>
Design, implement, and debug memory systems for persistent autonomous AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timesandplaces](https://clawhub.ai/user/timesandplaces) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to design durable memory systems for autonomous agents, including flat-file memory, semantic retrieval, and temporal knowledge graph patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable memory files can accumulate secrets, sensitive personal data, or stale operational state. <br>
Mitigation: Review memory files periodically, avoid storing secrets or sensitive personal data, and verify current runtime facts before consequential actions. <br>
Risk: Optional Graphiti or Neo4j setup introduces persistent services and package installation into the user's environment. <br>
Mitigation: Run optional persistent-service setup only in environments where those services and package installs are acceptable. <br>
Risk: OpenClaw gateway tokens may be exposed if copied into durable memory or shared configuration. <br>
Mitigation: Protect gateway tokens and avoid writing credentials into long-lived memory files. <br>


## Reference(s): <br>
- [Morrow Agent Memory on ClawHub](https://clawhub.ai/timesandplaces/morrow-agent-memory) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [Memory Architecture Reference](references/memory-architecture.md) <br>
- [Temporal Memory Discipline](references/temporal-discipline.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline code and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include memory file structures, temporal annotation conventions, and optional setup guidance for persistent services.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
