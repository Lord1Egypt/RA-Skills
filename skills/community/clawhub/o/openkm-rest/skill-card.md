## Description:

OpenKM Document Management via REST API (folders, documents, metadata, versioning, search, workflows).

This skill is ready for commercial/non-commercial use.

## Publisher:

[pes0](https://clawhub.ai/user/pes0)

### License/Terms of Use:


## Use Case:

Developers and operations teams use this skill to operate an OpenKM document repository through a local REST CLI for folder management, document upload and download, metadata updates, versioning, search, and workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change or delete OpenKM repository data using reusable credentials.

Mitigation: Use a least-privileged account and require explicit human confirmation before delete, restore, workflow, metadata, move, rename, checkin, or upload-version operations.

Risk: The skill does not enforce HTTPS for OPENKM_BASE_URL.

Mitigation: Require an HTTPS OPENKM_BASE_URL before installing or using the skill in a real OpenKM environment.

Risk: Download operations write to caller-selected local paths and may overwrite local files.

Mitigation: Review destination paths before execution and write downloads only to controlled workspace locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pes0/skills/openkm-rest)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python, OPENKM_BASE_URL, OPENKM_USERNAME, and OPENKM_PASSWORD.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
