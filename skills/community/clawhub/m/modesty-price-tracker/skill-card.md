## Description: <br>
Monitor product prices across Amazon, eBay, Walmart, and Best Buy to identify arbitrage opportunities and profit margins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modestyrichards](https://clawhub.ai/user/modestyrichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search product listings, compare prices across major retail platforms, calculate potential arbitrage margins, and generate price-monitoring reports or alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Price-history and trend outputs may be presented as market history even though the security review says they are simulated. <br>
Mitigation: Treat price-history and trend outputs as simulated unless the publisher replaces them with verifiable historical data or clearly labels them. <br>
Risk: The skill requires a SkillBoss API key and may send product lists or search terms to SkillBoss for processing. <br>
Mitigation: Use a dedicated revocable API key and avoid submitting confidential product lists unless SkillBoss processing is acceptable. <br>
Risk: Price lookups and arbitrage margins can be stale, incomplete, or misleading for spending decisions. <br>
Mitigation: Verify prices directly on retailer sites and review fees, shipping, taxes, seller reliability, and return risk before making purchases. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/modestyrichards/modesty-price-tracker) <br>
- [SkillBoss setup guide](https://skillboss.co/skill.md) <br>
- [SkillBoss API Hub endpoint](https://api.skillboss.co/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, CSV, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include current price tables, arbitrage margin calculations, alert text, and simulated price-history or trend data.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
