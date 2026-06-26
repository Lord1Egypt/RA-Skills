## Description: <br>
Guided interview to generate a complete agent workspace: SOUL.md, IDENTITY.md, MEMORY.md, AGENTS.md, USER.md with hierarchical memory structure, atomic facts, epistemic standards, anti-sycophancy rules, dissent protocol, and agent personality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[corbin-breton](https://clawhub.ai/user/corbin-breton) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use Persona Builder to run a structured interview and generate local workspace files that define an agent's identity, memory structure, communication preferences, autonomy bounds, schedule, epistemic standards, and anti-sycophancy behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated persona, memory, and authority files can durably shape future agent behavior. <br>
Mitigation: Review every generated file before use and remove or tighten any autonomy, sub-agent, background-loop, usage-tracking, or pruning instructions that are not intended. <br>
Risk: Interview answers and generated files can contain sensitive personal details such as schedule, goals, risks, and operating preferences. <br>
Mitigation: Do not enter unnecessary secrets or personal details, redact sensitive content, and avoid committing generated files to public or shared repositories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/corbin-breton/persona-builder) <br>
- [Interview blocks](artifact/references/interview-blocks.md) <br>
- [Generation rules](artifact/references/generation-rules.md) <br>
- [Research notes](artifact/references/research-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces SOUL.md, IDENTITY.md, MEMORY.md, AGENTS.md, and USER.md in the current workspace for user review and customization.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
