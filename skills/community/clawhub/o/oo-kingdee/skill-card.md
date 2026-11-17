## Description:

Connects to Kingdee Galaxy Enterprise through OOMOL to read, create, update, and delete business data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use the skill to work with Kingdee Galaxy Enterprise records through an OOMOL-connected account. It supports record queries and views as well as approved business data changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer and connector runtime were not validated by the artifact review, and automatic skill synchronization may change other agents' skills.

Mitigation: Review and approve CLI installation separately using a reviewed, pinned release with integrity verification, and review automatic skill synchronization before first use.

Risk: OOMOL mediates enterprise requests and connection credentials, while Kingdee actions can change or delete business data.

Mitigation: Use an appropriately limited Kingdee account and approve the exact write targets and payloads before execution.

Risk: The bundled API index is missing, limiting object-discovery workflows.

Mitigation: Restore the missing API index before relying on object discovery, and verify operation details against current official documentation.

## Reference(s):

- [Kingdee API documentation](https://open.kingdee.com/K3Cloud/Open/ApiCenterReportDetail.aspx)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Kingdee contract lookup and proxy requests](references/proxy-reference.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Text summaries and structured JSON returned by Kingdee actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the requested object and action; batch changes may report partial success.]

## Skill Version(s):

1.1.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
