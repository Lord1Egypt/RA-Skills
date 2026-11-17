## Description:

Parse raw WhatsApp exports (TXT or JSON) into normalized message objects with `timestamp`, `sender`, and `content`.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vishalgojha](https://clawhub.ai/user/vishalgojha)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to convert user-provided WhatsApp chat exports into validated timestamp, sender, and content records before downstream extraction workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WhatsApp exports can contain sensitive personal data.

Mitigation: Only provide chat exports that the user intends the agent to process, and keep downstream handling limited to the requested parsing workflow.

Risk: Malformed or ambiguous chat lines could produce invalid structured records.

Mitigation: Return explicit parse errors with line offsets when available and fail closed if the parsed output cannot satisfy the schema.

## Reference(s):

- [Parsed Message Array Schema](references/parsed-message-array.schema.json)
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Validated JSON array of message objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each message object contains timestamp, sender, and content; output preserves source order and fails closed when validation cannot pass.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
