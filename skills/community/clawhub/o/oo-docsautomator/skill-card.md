## Description:

Operate DocsAutomator for reading, creating, and updating data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to inspect DocsAutomator action schemas, read workspace information, and generate documents through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup recommends a remote CLI installer whose contents and hosted connector behavior are unverified; document generation actions can write to DocsAutomator.

Mitigation: Review and approve CLI installation separately, prefer a verified pinned release, and retain confirmations before document-writing actions.

## Reference(s):

- [DocsAutomator API documentation](https://docsautomator.co/docs/)
- [DocsAutomator website](https://www.docsautomator.co)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [DocsAutomator on ClawHub](https://clawhub.ai/oomol/skills/oo-docsautomator)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Text and Markdown, including document links or job status when returned]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include generated document URLs and execution status.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
