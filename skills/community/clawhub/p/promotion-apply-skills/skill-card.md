## Description:

Guides agents through Lingqu Banner promotion creation, querying, copying, updates, status transitions, creative setup, and linked material management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cloudmusiccio](https://clawhub.ai/user/cloudmusiccio)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operations agents use this skill to manage Lingqu Banner promotions through MWS, including schedule reservation, admin assignment, creative payload validation, and image upload workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make real banner promotion changes, add promotion admins, and upload assets.

Mitigation: Use it only in a trusted MWS environment with appropriate authorization, dry-run checks where supported, and human confirmation before write operations.

Risk: Helper scripts may install Python dependencies at runtime.

Mitigation: Remove runtime package installation before deployment and pin required dependencies in the execution environment.

Risk: Image tooling can download remote image URLs without an allowlist.

Mitigation: Restrict remote image downloads to approved domains or require local files before processing and upload.

Risk: NOS upload tokens are used during image upload workflows.

Mitigation: Store tokens only in a private temporary directory and clean them up immediately after upload.

## Reference(s):

- [Creative Dynamic Material Reference](references/creative-dynamic-material.md)
- [Image Upload NOS Reference](references/image-upload-nos.md)
- [MWS Shared Reference](references/mws-shared.md)
- [Phase One Reserve Reference](references/phase-one-reserve.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Markdown]

**Output Format:** [Markdown guidance with MWS shell commands, JSON payloads, and validation instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local validation files, resized image assets, and promotion-update payloads during agent execution.]

## Skill Version(s):

1.0.11 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
