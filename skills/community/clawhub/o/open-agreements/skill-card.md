## Description:

Fill standard legal agreement templates such as NDAs, cloud service agreements, and SAFEs, then produce signable DOCX files with optional DocuSign electronic-signature sending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and business teams use this skill to draft or fill standard legal agreement templates, generate reviewable DOCX files, and optionally send completed agreements for electronic signature.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agreement templates, signer details, and field values may contain confidential or regulated legal and business information, and the remote MCP path sends those values to openagreements.org.

Mitigation: Prefer the local CLI path for sensitive documents and use the hosted remote MCP only when the user accepts transmitting agreement data to the service.

Risk: The artifact documents a legacy hosted DocuSign connection URL that places an API key in the URL.

Mitigation: Avoid the legacy API-key URL flow and use the OAuth-based hosted authorization or local MCP signing-provider flow described by the skill.

Risk: Filled agreements may be sent to DocuSign for signature and can create real signing workflows.

Mitigation: Require user review and confirmation before sending any completed agreement for electronic signature.

Risk: The generated agreement may include legal terms, statutory-compliance representations, or template clauses that the agent cannot independently verify.

Mitigation: Ask the human to confirm required factual representations, leave unconfirmed statutory fields false, and remind users to review the document with qualified counsel when appropriate.

Risk: Installing or running the CLI through npm or npx can fetch executable package code.

Mitigation: Use pinned versions, avoid elevated privileges for npm commands, and review the package source before installing in sensitive environments.

## Reference(s):

- [Open Agreements GitHub Repository](https://github.com/open-agreements/open-agreements)
- [Open Agreements Remote MCP](https://openagreements.org/api/mcp)
- [open-agreements npm Package](https://www.npmjs.com/package/open-agreements)
- [Open Agreements Product Page](https://usejunior.com/developer-tools/open-agreements)
- [ClawHub Skill Page](https://clawhub.ai/stevenobiajulu/skills/open-agreements)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with MCP tool calls, JSON values, shell commands, and DOCX or download-link outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create signable DOCX files or hosted download URLs; local CLI flows should use per-run temporary JSON files for confidential field values.]

## Skill Version(s):

0.2.4 (source: evidence.json release.version and metadata.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
