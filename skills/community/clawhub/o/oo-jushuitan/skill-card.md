## Description:

Use a connected OOMOL account to read and manage Jushuitan ERP data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Operations and ERP users use this skill to query Jushuitan records and manage orders, inventory, purchasing, products, warehouse workflows, and finance data through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required oo CLI may install or update skills across agent environments; its remote installers and hosted connector remain unverified.

Mitigation: Review CLI installation and skill-management behavior, install a verified release, and consider setting OO_SKILLS_SYNC_DISABLED=1 before invoking it.

Risk: Write and destructive actions can change ERP records.

Mitigation: Confirm the exact payload and effect before write actions, and get explicit approval for destructive actions. Share only necessary tracking fields.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [Jushuitan OpenWeb API documentation](https://openweb.jushuitan.com/dev-doc)
- [Jushuitan FAQ: shipment tracking API limitation](https://openweb.jushuitan.com/qaCenter?groupId=12&postId=39)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON ERP responses, concise natural-language guidance, and oo CLI shell commands for actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live action schemas guide requests. Write actions require confirmation, and destructive actions require explicit approval. Shipment records do not include tracking events.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
