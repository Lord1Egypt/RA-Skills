## Description: <br>
Track and manage homelab hardware inventory, including purchase details, warranty dates, power draw, physical location, spend summaries, and insurance-ready reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Homelab owners and operators use this skill to maintain a local JSON inventory of hardware assets, answer questions about spend, warranties, locations, and power costs, and generate Markdown reports for operational or insurance review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Inventory files and command output may contain private asset details such as serial numbers, locations, purchase prices, and notes. <br>
Mitigation: Keep the inventory file private, avoid storing secrets, and avoid running searches or reports in shared terminals. <br>


## Reference(s): <br>
- [Common Homelab Device Power Draw Estimates](references/power-estimates.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/newageinvestments25-byte/homelab-assets) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, JSON, terminal tables, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local JSON inventory file; reports may include private asset details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
