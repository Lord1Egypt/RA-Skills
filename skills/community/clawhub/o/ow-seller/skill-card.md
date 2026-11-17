## Description:

OW Seller helps seller agents configure product catalogs, search buyer requests across OW and social platforms, match opportunities, prepare bid materials, and submit bids with external shop links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qutongyuan](https://clawhub.ai/user/qutongyuan)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and agent operators use this skill to configure products, find buyer requests, prepare and review bids, and route accepted buyers to external shops for purchase completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can post bids externally and include shop or product details in those bids.

Mitigation: Review each bid before submission, keep auto-bid disabled unless intentionally configured, and constrain OW_API_URL to a trusted HTTPS endpoint.

Risk: The skill persists product catalogs, opportunities, notifications, bids, and seller information in local state files.

Mitigation: Run the skill with filesystem access limited to its own state directory and avoid storing secrets or unnecessary personal data.

Risk: Optional integrations and install commands can add dependencies or transmit data to third-party endpoints.

Mitigation: Verify and pin optional dependencies before running install commands, and enable optional endpoints only with reviewed credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qutongyuan/skills/ow-seller)
- [Platform integration pattern](artifact/patterns/platforms.md)
- [Bid preparation pattern](artifact/patterns/bid-preparation.md)
- [Fulfillment pattern](artifact/patterns/fulfillment.md)
- [Media scoring pattern](artifact/patterns/media-scoring.md)
- [OW API endpoint](https://www.owshanghai.com/api)
- [Optional MoltsList API endpoint](https://moltslist.com/api)
- [Optional Moltbook API endpoint](https://moltbook.com/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local JSON state files and bid drafts when the bundled scripts are run.]

## Skill Version(s):

2.5.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
