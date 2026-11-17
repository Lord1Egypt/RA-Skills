## Description:

Full-featured YAML toolkit for validating, formatting, converting, merging, and querying YAML files. Supports YAML-to-JSON, JSON-to-YAML, schema validation, path queries, and multi-document YAML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to validate, format, convert, query, patch, merge, lint, and inspect YAML or JSON configuration files in local development, DevOps, CI/CD, data pipeline, and documentation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can write output to a user-specified path, which could overwrite important configuration files if used carelessly.

Mitigation: Review output paths before using --output, write to a temporary file first for important configurations, and compare changes before replacing originals.

Risk: Full multi-document YAML handling is not supported across every command, even though validation can read multiple documents.

Mitigation: Use multi-document YAML support only for validation unless each document is split or the transformed output is manually reviewed.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash examples, plus YAML, JSON, and plain-text command output from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated YAML or JSON to stdout or to a user-specified output file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
