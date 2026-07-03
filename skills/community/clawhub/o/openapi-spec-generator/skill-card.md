## Description: <br>
Auto-generate OpenAPI 3.x specs from code, traffic logs, or packet captures with interactive refinement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to draft OpenAPI 3.x documentation from source code, HTTP captures, traffic logs, packet captures, or manual endpoint descriptions. It can also help review an existing OpenAPI file and produce mock-server configuration guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled script is assessed as demo-quality while the documentation presents it as a real generator and validator. <br>
Mitigation: Treat generated specifications and validation reports as drafts, and verify them with trusted OpenAPI tooling and human review before using them for production documentation or security decisions. <br>
Risk: Code repositories, HAR files, traffic logs, and packet captures can contain credentials, internal hostnames, or personal data. <br>
Mitigation: Use sanitized inputs where possible, review generated output for sensitive data, and do not rely on the skill for secret-redaction guarantees. <br>
Risk: Generated files may overwrite existing output paths. <br>
Mitigation: Run the skill in a disposable workspace or write to reviewed output paths before replacing existing API documentation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/openapi-spec-generator) <br>
- [Source Detection Patterns](references/source-detection.yaml) <br>
- [Input Schema](https://openclaw.dev/skills/openapi-spec-generator/input.schema.json) <br>
- [Output Schema](https://openclaw.dev/skills/openapi-spec-generator/output.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, OpenAPI YAML or JSON snippets, validation reports, and optional Prism mock-server configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated specifications and validation findings should be reviewed before production use, especially when source inputs may contain secrets or sensitive traffic data.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, skill.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
