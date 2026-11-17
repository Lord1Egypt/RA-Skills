## Description:

Robust JSON parsing and validation with Pydantic schemas, JSON Schema validation, batch processing, and automatic JSON repair for LLM outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kikikari](https://clawhub.ai/user/kikikari)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to parse, repair, validate, and batch-process JSON from files, tool outputs, LLM responses, and JSON-Lines workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency version drift could change parsing or validation behavior.

Mitigation: Install the skill in a virtual environment and pin pydantic, json-repair, and jsonschema versions before use.

Risk: validate_tool_output.py is a convenience validator and may not meet strict JSON Schema enforcement needs.

Mitigation: Use json_schema_validator.py for full JSON Schema validation when strict schema enforcement is required.

Risk: German-heavy documentation may be misunderstood by non-German users.

Mitigation: Review the API reference and script behavior carefully, or translate the documentation before operational use.

## Reference(s):

- [JSON Utils API Reference](references/api_reference.md)
- [ClawHub Skill Page](https://clawhub.ai/kikikari/skills/json-utils)
- [Publisher Profile](https://clawhub.ai/user/kikikari)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline Python, shell, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce parsed JSON objects, validation results, batch result summaries, and error messages.]

## Skill Version(s):

1.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
