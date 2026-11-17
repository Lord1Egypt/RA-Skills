## Description:

Uploads local or inbound product media to MaybeAI, runs the upload-audit workflow pipeline, generates an HTML audit report, and can share the report through a trycloudflare URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ojbkxiongdei](https://clawhub.ai/user/ojbkxiongdei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to upload product images or videos to MaybeAI, run copy, analyze, audit, font-audit, and summary workflows, and return spreadsheet, report, and sharing outputs for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public trycloudflare sharing can expose more local files than the intended report if it serves a broad workspace or sensitive folder.

Mitigation: Use --share only from a clean report directory, review what the local HTTP server can access, treat the URL as public and unauthenticated, and stop the tunnel when finished.

Risk: The workflow requires live MaybeAI bearer tokens and user IDs, which can be exposed through shell history, logs, or shared command snippets.

Mitigation: Use test or least-privilege credentials, avoid pasting bearer tokens into persistent shell history, redact logs before sharing, and rotate credentials after risky use.

Risk: Uploaded media, spreadsheet rows, and generated audit reports may contain confidential product or compliance information.

Mitigation: Confirm authorization before uploading media, avoid public sharing for sensitive audits, and remove generated reports and copied spreadsheets when no longer needed.

## Reference(s):

- [Live Run Notes](references/live-run-notes.md)
- [Protocol Notes](references/protocol-notes.md)
- [MaybeAI Upload Audit Page](https://maibei.maybe.ai/e-commerce/upload-audit-file)
- [MaybeAI Source Spreadsheet](https://www.maybe.ai/docs/spreadsheets/d/69c2400ea25ba20198828d73?gid=0)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands, JSON workflow payloads, streamed workflow output, and optional self-contained HTML report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return uploaded media URLs, copied spreadsheet URLs, workflow event logs, local report paths, and public trycloudflare report URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
