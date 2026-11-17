## Description:

Generates API and technical documentation from source code, including comment extraction, Chinese documentation templates, OpenAPI 3.0 output, and optional Feishu document publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[penghang1223](https://clawhub.ai/user/penghang1223)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect selected Python, JavaScript/TypeScript, or Go source files and produce API documentation, local Markdown, OpenAPI YAML/JSON, or Feishu-ready documentation for team use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated documentation may expose internal endpoints, schemas, comments, or secrets when saved broadly or sent to Feishu.

Mitigation: Review generated output for sensitive implementation details before sharing or publishing it.

Risk: Static extraction can miss dynamic routes or misstate parameters, return values, and errors.

Mitigation: Compare generated documentation against the selected source files and update any incomplete API details before use.

## Reference(s):

- [OC Doc Generator on ClawHub](https://clawhub.ai/penghang1223/skills/oc-doc-generator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, OpenAPI YAML/JSON, and Feishu-flavored Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated documentation to stdout or a user-selected output path; Feishu publication depends on a separate Feishu document tool.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
