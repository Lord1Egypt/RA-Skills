## Description:

Track, manage, and report on homelab hardware inventory with purchase, warranty, power use, location, and insurance-ready reporting details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Homelab operators and technical users use this skill to maintain a local hardware inventory, inspect warranties and locations, estimate power costs, and generate insurance-ready Markdown reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Homelab inventory records and reports can expose serial numbers, purchase prices, service notes, and physical locations stored in local plaintext JSON.

Mitigation: Keep inventory files and generated reports private, restrict filesystem access to the inventory path, and remove or replace sensitive values before sharing JSON, search output, reports, or examples.

## Reference(s):

- [Common Homelab Device Power Draw Estimates](references/power-estimates.md)
- [Example Homelab Inventory JSON](assets/inventory.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text, JSON, and Markdown reports with shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local inventory JSON file, defaulting to ~/.openclaw/workspace/homelab-assets/inventory.json or a path set with HOMELAB_ASSETS_PATH.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
