## Description:

Use the OOMOL-connected Megaventory account to read inventory and order data, and create or update products and orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Operations and inventory teams use this skill to look up products, locations, suppliers, clients, and sales or purchase orders in Megaventory, and to create or update products and orders through their OOMOL-connected account. Confirm the exact payload and effect before making changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Megaventory write actions change product or order records.

Mitigation: Confirm the exact payload and effect with the user before running a write action.

Risk: The required oo CLI may change other agents’ installed skills, and the remote installer could not be inspected; an unpinned installation may not establish which release will be delivered.

Mitigation: Review CLI setup, use a verified CLI release, and consider setting OO_SKILLS_SYNC_DISABLED=1 before each oo invocation. Verify the connected business account before approving changes.

## Reference(s):

- [Megaventory](https://www.megaventory.com/)
- [Megaventory API documentation](https://help.megaventory.com/en/articles/74873-how-do-i-get-started-with-the-api)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Megaventory ClawHub skill page](https://clawhub.ai/oomol/skills/oo-megaventory)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Connector data returned as JSON with concise natural-language summaries and action guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions return Megaventory data; product and order writes require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
