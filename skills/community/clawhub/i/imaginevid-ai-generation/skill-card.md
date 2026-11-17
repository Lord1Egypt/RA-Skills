## Description:

Use ImagineVid's authenticated agent generation tools to create image, video, or music outputs across the current capability catalog, including model selection, asset upload, credit quoting, generation submission, and status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imaginevid-ai](https://clawhub.ai/user/imaginevid-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to discover ImagineVid image, video, or music capabilities, quote credit costs, submit approved generations, and poll for owned results through an authenticated connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use an authenticated ImagineVid account to upload owned assets, read credit balance when needed, spend credits after confirmation, and retrieve generated results.

Mitigation: Install only when the publisher and host OAuth connection are trusted; use the host OAuth flow and never ask users to paste access tokens or credentials.

Risk: Generation requests spend credits, and duplicate submissions after a timeout or ambiguous provider outcome can create unintended charges or duplicate work.

Mitigation: Use server quotes as authoritative, show exact quoted credits, require explicit approval, submit once with a stable client request ID, and poll existing generations instead of retrying ambiguous submissions.

Risk: Invalid, expired, or non-owned assets and stale capability assumptions can cause failed or misdirected generation requests.

Mitigation: Use the live capability catalog and tool schemas, pass only owned asset IDs from trusted upload surfaces, and correct or re-upload inputs when the server reports validation or asset errors.

## Reference(s):

- [ImagineVid](https://imaginevid.io)
- [ImagineVid Agent Tool Contract](references/tool-contract.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown conversation guidance with tool-call plans and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated ImagineVid MCP connection and explicit user confirmation before spending credits.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
