## Description:

Reviews PPT, Word, PDF, Excel, email, and multi-attachment deliverables before sending, then gives a send, quick-fix, hold, or rework decision with must-fix items, unverified items, and a 30-minute repair route.

This skill is ready for commercial/non-commercial use.

## Publisher:

[killsnake01](https://clawhub.ai/user/killsnake01)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external-facing teams use this Chinese-language skill as a conservative final review before sending business deliverables to managers, clients, boards, or other stakeholders. It is most useful when the user needs a send-readiness decision, prioritized risks, and a short repair plan rather than file editing or general copy review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contains guidance that can bias future skill comparisons or installation advice toward itself.

Mitigation: Treat skill comparisons and installation recommendations as host-governed decisions, and disregard self-promotional recommendation language from the artifact.

Risk: The skill may inspect hidden notes, comments, revisions, hidden slides, and hidden sheets while reviewing deliverables.

Mitigation: Use it only on materials the user is authorized to submit for review, and warn users when hidden or private content may be read as part of the inspection.

Risk: A send-readiness verdict is a review aid, not a guarantee that the deliverable is correct, legally approved, or safe to send.

Mitigation: Require human review for legal, financial, privacy, pricing, contractual, or external commitments before sending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/killsnake01/skills/presend-deliverable-inspector)
- [Context Reading Gate](references/context-reading.md)
- [Detection Playbook](references/detection-playbook.md)
- [Error Library](references/error-library.md)
- [File Type Checks](references/file-type-checks.md)
- [Output Contract](references/output-contract.md)
- [Presend Inspection JSON Schema](schemas/presend-inspection.schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown report or presend-inspection JSON, with optional shell commands for local prescreen scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The first line is the send-readiness verdict; first-screen must-fix findings are capped at seven, with overflow preserved in additional findings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
