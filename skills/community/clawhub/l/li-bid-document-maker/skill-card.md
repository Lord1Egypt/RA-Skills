## Description:

Automatically convert tender documents (PDF/Word) into professional response bid documents following Chinese bidding standards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[43622283](https://clawhub.ai/user/43622283)

### License/Terms of Use:

MIT-0

## Use Case:

External users, proposal teams, and bid-document specialists use this skill to turn tender or RFP files into structured bid responses, including tender parsing, scoring strategy, chapter drafting, quality checks, and PDCA improvement reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads tender files that may contain confidential pricing, personal data, or business-sensitive requirements.

Mitigation: Install and invoke it only in a trusted project environment, restrict file access to the relevant folder, and review or redact sensitive tender content before use.

Risk: Generated bid responses may contain incorrect, incomplete, or unsupported claims.

Mitigation: Have proposal owners review the final document, quality report, evidence references, legal sections, and scoring coverage before submission.

Risk: Optional PDF, Word, OCR, and OpenClaw dependencies can expand the local execution surface.

Mitigation: Use pinned, trusted package versions and install only the optional components required for the selected workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/43622283/skills/li-bid-document-maker)
- [English Usage Guide](artifact/docs/README.en.md)
- [Workflow Pipeline](artifact/references/workflows/pipeline.yaml)
- [Tender Info Schema](artifact/references/schemas/tender-info.schema.json)
- [Bid Document Schema](artifact/references/schemas/bid-document.schema.json)
- [Bid Structure Template](artifact/references/templates/bid-structure.json)
- [Format Rules](artifact/references/templates/format-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown reports and structured JSON summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a bid response document, PDCA quality improvement report, and scoring criteria mapping; optional file processing depends on the agent environment.]

## Skill Version(s):

0.0.2 (source: SKILL.md frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
