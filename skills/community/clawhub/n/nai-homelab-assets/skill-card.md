## Description: <br>
Track, manage, and report on homelab hardware inventory, including purchase details, warranty dates, power use, location, and insurance-ready asset reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, homelab operators, and technical users use this skill to maintain a local hardware inventory, search assets, check warranties, estimate power costs, and generate asset reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Inventory files and generated reports can reveal owned equipment, physical locations, serial numbers, purchase prices, and operational notes. <br>
Mitigation: Keep the inventory JSON and generated reports private, avoid sharing them publicly, and remove sensitive fields before sending reports to others. <br>


## Reference(s): <br>
- [Common Homelab Device Power Draw Estimates](references/power-estimates.md) <br>
- [Example inventory structure](assets/inventory.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration] <br>
**Output Format:** [Markdown reports, JSON inventory data, terminal text, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads and writes a local inventory JSON file; reports can be written to Markdown.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
