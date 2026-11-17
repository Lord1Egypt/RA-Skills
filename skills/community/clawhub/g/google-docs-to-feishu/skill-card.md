## Description:

Syncs or copies Google Docs content into Feishu Docs with manual, automated conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[turbos7](https://clawhub.ai/user/turbos7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and productivity users use this skill to move Google Docs content into Feishu Docs while preserving common document structures such as headings, paragraphs, lists, tables, and images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted document content could affect local shell command construction during sync.

Mitigation: Install only after the publisher replaces shell command construction with execFile or spawn argument arrays, or uses a direct Feishu API or SDK.

Risk: Google credential and OAuth token files are stored on disk.

Mitigation: Treat these files as secrets and restrict them to owner-only access before use.

Risk: The configured Google OAuth scopes include profile and email access beyond readonly document access.

Mitigation: Remove the unused profile and email scopes unless the publisher documents why they are required.

Risk: Document content is copied from Google Docs into Feishu.

Mitigation: Review documents before syncing so sensitive or unintended content is not transferred.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/turbos7/skills/google-docs-to-feishu)
- [Google Cloud Console](https://console.cloud.google.com)
- [Google Docs readonly OAuth scope](https://www.googleapis.com/auth/documents.readonly)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and JSON-like sync results with document title, status, and Feishu document identifiers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update Feishu documents through configured Feishu tooling and local OAuth credentials.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
