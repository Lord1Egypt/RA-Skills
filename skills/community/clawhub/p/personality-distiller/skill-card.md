## Description: <br>
Personality Distiller automatically distills a name, vague requirement, link, existing skill, or local corpus into a complete agent persona file pack through research and framework extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to convert source material about a person, thinking model, existing skill, web page, or local corpus into a structured persona for an agent workspace. It is intended for persona generation workflows that need research, extraction, mapping, and a final review step before overwriting persona files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local corpus files that may contain sensitive personal material. <br>
Mitigation: Provide only the specific files or folders intended for analysis and avoid secrets or highly sensitive personal material unless that exposure is deliberate. <br>
Risk: The skill is designed to overwrite persistent workspace persona files. <br>
Mitigation: Back up existing persona files and require explicit confirmation before any overwrite. <br>


## Reference(s): <br>
- [Deep Research Guide for Persona Distillation](artifact/references/research-guide.md) <br>
- [Persona Dimensions & Mapping Guide](artifact/references/persona-dimensions.md) <br>
- [Thinking Frameworks Catalog](artifact/references/frameworks.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown persona file pack with summary guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates SOUL.md, IDENTITY.md, USER.md, AGENTS.md, TOOLS.md, and HEARTBEAT.md for the workspace after the required confirmation workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
