## Description: <br>
Helps agents research Amazon product opportunities by scouting demand, filtering niches, benchmarking products, mining review pain points, checking IP signals, and producing a go/no-go report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pangolinfo](https://clawhub.ai/user/pangolinfo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, product teams, and e-commerce researchers use this skill to evaluate Amazon product categories and niches before launching a new product. It guides an agent through fast and full research modes that combine demand signals, benchmark products, review themes, IP checks, and investment recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Pangolinfo API key in the runtime environment. <br>
Mitigation: Treat the API key as a secret, provide it through the supported environment or MCP configuration path, avoid pasting it into prompts or logs, and rotate it if exposure is suspected. <br>
Risk: Full-mode and review-scraping workflows can consume additional Pangolinfo credits. <br>
Mitigation: Use the fast mode by default, confirm budget before review scraping or full reports, and monitor quota usage. <br>
Risk: Amazon market and IP signals may be incomplete or time-sensitive. <br>
Mitigation: Use the report as decision support, review source-labeled findings before acting, and obtain professional IP review before product launch or large inventory commitments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pangolinfo/pangolinfo-amazon-product-explorer) <br>
- [Pangolinfo](https://www.pangolinfo.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown reports with tables, concise recommendations, and red/yellow/green go/no-go decisions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source-labeled market metrics, benchmark product comparisons, review themes, IP-risk notes, budget prompts, and next-step recommendations.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release metadata; artifact frontmatter says 3.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
