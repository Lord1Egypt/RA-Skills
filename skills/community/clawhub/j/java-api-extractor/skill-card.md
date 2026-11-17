## Description:

Extracts Java Spring Boot Controller API definitions into standardized JSON data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snowzhouj](https://clawhub.ai/user/snowzhouj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scan Java Spring Boot projects, extract Controller-layer endpoint definitions, and prepare standardized JSON API documentation for downstream documentation or product data workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanning Java source trees can expose internal API structure in generated outputs.

Mitigation: Run extraction locally first and review generated JSON before sharing or uploading it.

Risk: The scripts create extra local backup copies by default.

Mitigation: Use --no-backup when duplicate retained files are not desired, or manage the backup directory under approved retention controls.

Risk: The optional --push or --prdid flow can run a neighboring upload script.

Mitigation: Use push options only after reviewing the neighboring push script and approving the destination and uploaded contents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snowzhouj/skills/java-api-extractor)
- [API definition standard](references/api-definition-standard.md)
- [Usage examples](references/usage-examples.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with optional shell commands and generated JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The extraction scripts can write an output JSON file and create a backup copy unless the user passes --no-backup.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
