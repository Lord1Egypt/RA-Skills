## Description:

Research a business website, produce a concise prospect report, recommend concrete OpenClaw use cases, and draft a tailored outreach email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lexalex36](https://clawhub.ai/user/lexalex36)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business development operators use this skill to turn a business website URL and contact email into a concise OpenClaw opportunity brief, outreach report, and approval-gated email draft.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled email-sending helper can send real Gmail messages without enforcing the documented approval gate.

Mitigation: Use drafting and rendering helpers only in a controlled workspace, and do not use the send script unless it defaults to dry-run, requires an explicit approved manifest, validates recipient and content hashes, and requires a configured sender account.

Risk: Generated email bodies and brief attachments can be sent outside the organization.

Mitigation: Treat generated bodies and attachments as outbound data and review the recipient, subject, body, and attachment before any approved send.

## Reference(s):

- [Outreach Demo Report Format](references/report-format.md)
- [Outreach Demo Email Template](references/email-template.md)
- [Value-First Outreach Mode](references/value-first-outreach.md)
- [Visual Delivery Mode](references/visual-delivery.md)
- [Follow-Up Sequence](references/follow-up-sequence.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Structured JSON, Markdown reports, plain-text email drafts, HTML email or brief files, PDF briefs, and preview manifests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-first workflow with an approval preview before outbound email; PDF rendering depends on Chromium and sending depends on a configured Gmail-compatible command.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
