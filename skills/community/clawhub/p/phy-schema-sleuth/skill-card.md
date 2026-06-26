## Description: <br>
Infer clean, production-ready schemas from messy sample data and return Pydantic, Zod, TypeScript, JSON Schema, or Go schema artifacts with inferred types, nullability, optional fields, and validation rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn representative samples of JSON, CSV, API responses, plain text, or LLM output into schema definitions and typed models for application development and validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may paste secrets, customer records, internal URLs, or other confidential data as schema samples. <br>
Mitigation: Redact sensitive values before using the skill and prefer synthetic or minimized examples. <br>
Risk: Schema inference from a small number of samples can produce incomplete types, optionality, enum values, or validation rules. <br>
Mitigation: Review generated schemas against the real domain model before production use. <br>


## Reference(s): <br>
- [Phy Schema Sleuth on ClawHub](https://clawhub.ai/PHY041/phy-schema-sleuth) <br>
- [PHY041 publisher profile](https://clawhub.ai/user/PHY041) <br>
- [Canlah AI](https://canlah.ai) <br>
- [JSON Schema Draft 7](http://json-schema.org/draft-07/schema#) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown report with field analysis and fenced code blocks for generated schemas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Pydantic v2 models, Zod schemas, TypeScript interfaces, JSON Schema Draft 7, Go structs, parser snippets, and confidence notes.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
