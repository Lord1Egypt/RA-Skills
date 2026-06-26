## Description: <br>
Monitor product prices across Amazon, eBay, Walmart, and Best Buy to identify arbitrage opportunities and profit margins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business users use this skill to search e-commerce prices, compare cross-platform arbitrage opportunities, monitor products in bulk, and produce price, margin, alert, and history reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Historical price reports may present generated mock history as real market history. <br>
Mitigation: Do not rely on history, trend analysis, or predictions for business decisions unless the maintainer replaces the mock generation or clearly labels it as simulation. <br>
Risk: Product searches, monitored items, and derived search-result text are sent to SkillBoss. <br>
Mitigation: Use only when comfortable sharing those inputs with SkillBoss and avoid submitting sensitive product or business information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirkraman/godfery-price-tracker) <br>
- [SkillBoss API Hub endpoint](https://api.skillbossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, CSV, and command-line text reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and may write alert reports when an output path is supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
