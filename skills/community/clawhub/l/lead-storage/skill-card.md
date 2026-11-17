## Description:

Persist validated lead objects through write-only storage operations after Supervisor provides explicit confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vishalgojha](https://clawhub.ai/user/vishalgojha)

### License/Terms of Use:


## Use Case:

Real-estate operations teams and agent workflows use this skill to persist already validated lead records to write-only storage after supervisor confirmation, preserving normalized location, record type, and prioritization metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The approval gate may treat any non-empty confirmation token as sufficient before writing personal and business lead data.

Mitigation: Use only behind a trusted supervisor and storage service that independently verifies approval with signed, short-lived tokens bound to the exact lead payload.

Risk: Lead records include personal contact data and business context that should not be written on ambiguous or repeated requests.

Mitigation: Validate payloads against the input schema, fail closed on permission ambiguity, and enforce idempotency by lead_id.

## Reference(s):

- [Storage Input Schema](artifact/references/storage-input.schema.json)
- [Storage Output Schema](artifact/references/storage-output.schema.json)
- [ClawHub Skill Page](https://clawhub.ai/vishalgojha/skills/lead-storage)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON object with status, stored_ids, and error_message fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output should conform to artifact/references/storage-output.schema.json.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
