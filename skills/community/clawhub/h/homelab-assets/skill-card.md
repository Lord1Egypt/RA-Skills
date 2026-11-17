## Description:

Track and manage homelab hardware inventory, including servers, switches, UPS units, drives, cables, and accessories, with purchase details, warranty dates, power draw, physical locations, spend summaries, power-cost estimates, and insurance-ready reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte)

### License/Terms of Use:

MIT-0

## Use Case:

External users and homelab operators use this skill to maintain a local hardware inventory, answer questions about assets, warranty status, spend, and estimated power costs, and generate Markdown reports for planning or insurance documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local inventory can contain sensitive homelab details such as serial numbers, purchase prices, notes, warranty dates, and physical locations.

Mitigation: Store the inventory only in a trusted local path, restrict file permissions and backups, and avoid adding sensitive details that are not needed for asset tracking.

Risk: Broad hardware, warranty, and asset-tracking triggers may surface inventory details during general conversations.

Mitigation: Confirm the intended inventory lookup before using the skill for broad hardware or warranty questions when privacy matters.

Risk: Power-cost and depreciation values are estimates based on user-entered wattage, kWh rate, purchase dates, and straight-line depreciation assumptions.

Mitigation: Treat generated cost and value reports as planning aids, verify high-value assets manually, and measure power draw directly when accuracy is important.

## Reference(s):

- [Homelab Assets ClawHub page](https://clawhub.ai/newageinvestments25-byte/skills/homelab-assets)
- [Common Homelab Device Power Draw Estimates](references/power-estimates.md)
- [Example inventory JSON](assets/inventory.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance, files]

**Output Format:** [Plain text, JSON inventory data, and Markdown asset reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local JSON inventory file; report output can be written to a user-specified Markdown file.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
