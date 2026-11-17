## Description:

Draft and fill NDA templates, including mutual NDAs, one-way NDAs, and confidentiality agreements, using Common Paper and Bonterms standard forms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to collect NDA details, choose an appropriate mutual or one-way NDA template, and produce a signable DOCX or preview.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote MCP use can transmit confidential NDA details to a hosted third-party service.

Mitigation: Tell the user what data will be sent, get explicit informed consent, and offer the local CLI path for highly sensitive NDAs.

Risk: Local CLI use passes user-provided values into shell-driven document generation.

Mitigation: Pin open-agreements@0.7.5, allowlist the DOCX output filename, reject unsafe characters, and store values in a chmod 600 per-run temp file.

Risk: Generated NDA documents may not fit the user's legal needs.

Mitigation: Require review of the generated document before signing and recommend attorney review for non-standard terms.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/stevenobiajulu/skills/nda)
- [Open Agreements](https://openagreements.org)
- [Open Agreements Remote MCP](https://openagreements.org/api/mcp)
- [open-agreements on npm](https://www.npmjs.com/package/open-agreements)
- [Open Agreements README](https://github.com/open-agreements/open-agreements#use-with-claude-code)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Guidance]

**Output Format:** [DOCX files or download URLs, with Markdown preview output when rendering is unavailable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit confirmation before filling templates; local CLI use requires sanitized inputs and secure temporary files.]

## Skill Version(s):

0.2.3 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
