## Description:

Manage Kibana Saved Objects, including dashboards, Lens visualizations, imports, exports, bulk operations, references, and corrupted-object troubleshooting via the Kibana Saved Objects REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chunkin616-hue](https://clawhub.ai/user/chunkin616-hue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to manage Kibana dashboards, Lens visualizations, and related saved objects through REST API examples and helper scripts. It supports NDJSON import/export, bulk saved-object workflows, reference management, and troubleshooting for corrupted or missing saved-object dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Destructive Kibana operations can delete saved objects or overwrite imported dashboards and visualizations.

Mitigation: Require backups and explicit confirmation before delete operations or overwrite imports, and run against a controlled Kibana environment.

Risk: Cleartext HTTP defaults may expose Kibana traffic or credentials on untrusted networks.

Mitigation: Prefer HTTPS endpoints and avoid using the provided HTTP examples outside trusted local or internal environments.

Risk: The dashboard export helper builds a local filename from the dashboard ID.

Mitigation: Review or patch export filename handling before using untrusted dashboard IDs or untrusted Kibana endpoints.

## Reference(s):

- [Kibana Saved Objects ClawHub release](https://clawhub.ai/chunkin616-hue/skills/kibana-saved-objects)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python helper scripts and JSON or NDJSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes REST endpoint patterns, request bodies, troubleshooting notes, and scripts that can call Kibana APIs or read and write NDJSON files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
