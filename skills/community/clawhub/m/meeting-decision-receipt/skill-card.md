## Description:

Reviews existing meeting transcripts, minutes, notes, or discussion records to distinguish confirmed decisions, tentative items, proposals, explicit commitments, unconfirmed assignments, and intent-only statements, with short source evidence for each judgment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[killsnake01](https://clawhub.ai/user/killsnake01)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external collaborators, and agents use this skill to turn existing meeting text into evidence-grounded decision receipts and follow-up minutes. It is intended for checking what was decided, who explicitly accepted work, and what remains unconfirmed, not for audio transcription, verbatim transcript generation, employee evaluation, or automatic sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted meeting text can alter the generated Markdown minutes document.

Mitigation: Review generated Markdown before sharing or pasting it into Feishu or another Markdown-capable tool; prefer HTML output or trusted, sanitized source text until Markdown escaping is fixed.

Risk: Meeting inputs can contain credentials, contact details, or sensitive internal information.

Mitigation: Use the skill's redaction flow before evidence extraction, keep only short supporting evidence in outputs, and avoid external sharing for sensitive or high-stakes records.

Risk: Unconfirmed assignments or intent-only statements could be mistaken for accepted work.

Mitigation: Keep commitment labels evidence-bound, preserve missing confirmation as an open loop, and require explicit user confirmation before sending messages or creating tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/killsnake01/skills/meeting-decision-receipt)
- [classification-rules.md](artifact/references/classification-rules.md)
- [decision-taxonomy.md](artifact/references/decision-taxonomy.md)
- [commitment-taxonomy.zh-CN.md](artifact/references/commitment-taxonomy.zh-CN.md)
- [evidence-rules.md](artifact/references/evidence-rules.md)
- [output-style.md](artifact/references/output-style.md)
- [safety.md](artifact/references/safety.md)
- [receipt.schema.json](artifact/schemas/receipt.schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Structured JSON with Markdown or HTML meeting receipts and minutes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include decision status, commitment status, open loops, short evidence snippets, redaction state, and confirmation-message text; sending remains a separate user-confirmed action.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
