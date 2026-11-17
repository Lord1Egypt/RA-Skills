## Description:

Auto-generate OpenAPI 3.x specs from code, traffic logs, or packet captures with interactive refinement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to draft OpenAPI 3.x specifications from API source material such as code repositories, HAR files, traffic logs, packet captures, or manual endpoint descriptions. Review generated specs before production use, especially when inputs contain sensitive traffic data or when validation results affect public API documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security review reports that the shipped script returns canned analysis and validation results, so generated endpoint discovery, schemas, and pass/fail validation can be misleading.

Mitigation: Treat outputs as draft documentation only; manually review endpoint coverage, schemas, authentication details, and validation status before relying on them.

Risk: The generator can write to user-provided output paths and overwrite files.

Mitigation: Use non-critical output paths, keep backups or version control enabled, and inspect generated files before replacing existing API documentation.

Risk: Inputs such as HAR files and packet captures can contain authentication tokens, internal hostnames, or personally identifiable information.

Mitigation: Avoid sensitive captures unless necessary, redact secrets before sharing generated specs, and review outputs for leaked credentials or internal network details.

## Reference(s):

- [Openapi Spec Generator Skill Page](https://clawhub.ai/harrylabsj/skills/openapi-spec-generator)
- [source-detection.yaml](references/source-detection.yaml)
- [input.schema.json](schemas/input.schema.json)
- [output.schema.json](schemas/output.schema.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and generated YAML or JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate OpenAPI YAML/JSON specs, validation summaries, and optional Prism mock server configuration.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
