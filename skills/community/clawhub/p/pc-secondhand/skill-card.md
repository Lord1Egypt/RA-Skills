## Description:

Detects PC hardware config via PowerShell, estimates second-hand price for Xianyu (闲鱼), generates valuation report, product poster, and listing copy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this Windows-focused skill to collect local PC hardware details, estimate second-hand resale value for Xianyu, and generate HTML reports, poster material, listing copy, and selling guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local PowerShell inventory that records hardware and device details.

Mitigation: Use it only on a PC where local hardware inventory collection is acceptable, and review the generated inventory before sharing outputs.

Risk: The temporary pc_config.txt file may retain local hardware details after the workflow completes.

Mitigation: Delete the temporary pc_config.txt file after use if the inventory should not remain on disk.

Risk: Generated resale text could omit condition details or misstate defects.

Mitigation: Review and edit listing copy before posting so hardware condition, modifications, and defects are accurately disclosed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/pc-secondhand)
- [二手配件估价参考](references/price-guide.md)
- [咸鱼出售文案模板](references/listing-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with PowerShell commands and generated local HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a temporary pc_config.txt hardware inventory file, HTML valuation report, HTML Xianyu poster, listing copy, and an optional generated product image.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
