## Description: <br>
Generate structured Product Requirement Documents (PRDs) in Markdown, with optional Word (.docx) export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[casperkwok](https://clawhub.ai/user/casperkwok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers, product teams, and agents use this skill to turn rough product, module, or feature ideas into structured PRDs with the appropriate L0, L1, or L2 depth. It supports Markdown PRD generation by default and optional Word export when a local Node conversion flow is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Word export runs a local Node script and uses the npm docx package. <br>
Mitigation: Install the dependency only when Word export is needed, use a trusted package source, and run the converter only on PRD Markdown files intended for export. <br>
Risk: Broad PRD trigger phrases may activate the skill during general product discussion. <br>
Mitigation: Use explicit prompts or the /prd-generator invocation when PRD generation is desired, and ask the agent to remain in discussion mode when drafting should not start. <br>


## Reference(s): <br>
- [PRD Template](references/prd_template.md) <br>
- [PRD Writing Specification](references/writing_spec.md) <br>
- [PRD Creator on ClawHub](https://clawhub.ai/casperkwok/prd-creator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown PRD by default, with optional Word (.docx) file export through a local Node script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated PRDs follow a fixed section structure, Given-When-Then acceptance criteria, field tables, boundary exceptions, and a quality checklist.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
