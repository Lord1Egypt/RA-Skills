## Description: <br>
Write, review, or improve prompts for MindStudio Generate Text blocks, including plain-text prompts, structured JSON output, variable injection, conditional logic, and dot-notation access in workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sol1986](https://clawhub.ai/user/sol1986) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
MindStudio workflow builders and agent developers use this skill to design production-ready Generate Text block prompts. It helps them gather workflow context, use exact variable names, choose text or JSON output, and produce paste-ready prompt templates with sample JSON outputs when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated prompts can include incorrect, incomplete, or misleading instructions if the workflow context or variable names are wrong. <br>
Mitigation: Review generated prompts before deploying them and confirm that every referenced variable, output schema, and downstream access pattern matches the MindStudio workflow. <br>
Risk: Some examples involve privacy-sensitive lead enrichment or email-finding workflows. <br>
Mitigation: Use those patterns only with authorization, a lawful basis, and compliance with applicable privacy and anti-spam requirements. <br>
Risk: Sample JSON schemas and outputs may accidentally expose sensitive or unnecessary data when copied into a workflow. <br>
Mitigation: Sanitize sample schemas and example data before use, and include only fields needed by downstream blocks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sol1986/mindstudio-generate-text-block-prompting-skill) <br>
- [README](artifact/README.md) <br>
- [Examples](artifact/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, configuration, guidance] <br>
**Output Format:** [Markdown guidance with prompt templates, JSON schemas, realistic sample outputs, and MindStudio block-setting recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for user-reviewed prompts; it does not call external services or execute workflow actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
