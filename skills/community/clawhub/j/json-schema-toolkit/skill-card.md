## Description: <br>
Validate JSON data against JSON Schema, generate schemas from sample JSON, and convert schemas to TypeScript interfaces, Python dataclasses, or Markdown docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill for local JSON Schema validation, schema generation from examples, and conversion to TypeScript, Python dataclasses, or Markdown documentation during API contract and data workflow work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated TypeScript or Python may be incorrect for a downstream project if used without review. <br>
Mitigation: Review generated code before running, importing, or committing it. <br>
Risk: The bundled validator covers common JSON Schema keywords and skips reference resolution. <br>
Mitigation: Use it for basic local checks and use a full JSON Schema validator when schemas depend on $ref or unsupported keywords. <br>


## Reference(s): <br>
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, JSON, TypeScript, Python, and validation text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read JSON from stdin or local files and may write generated schema JSON when an output path is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
