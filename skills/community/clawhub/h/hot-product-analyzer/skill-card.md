## Description: <br>
Analyzes hot products across major Chinese e-commerce platforms and generates an interactive HTML report covering pricing, sales signals, keywords, selling points, visual style, and product-selection guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
E-commerce operators, product researchers, and sellers use this skill to research public marketplace signals for a product category and turn the findings into a concise hot-product analysis report. It is intended for market research and product-selection planning, not as a substitute for direct platform analytics or business due diligence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Marketplace prices, sales counts, ratings, and rankings are point-in-time public search signals and may be incomplete or inaccurate. <br>
Mitigation: Label generated figures as estimates, cite data sources in the report where available, and validate key conclusions against first-party platform analytics before business decisions. <br>
Risk: Generated reports load Chart.js from jsDelivr by default, which introduces an external network dependency when the HTML file is opened. <br>
Mitigation: Use the report in environments where that CDN dependency is acceptable, or replace it with a locally reviewed Chart.js asset before distributing the report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/hot-product-analyzer) <br>
- [Report template](artifact/assets/report_template.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Guidance, Files] <br>
**Output Format:** [Interactive single-file HTML report with textual analysis and Chart.js visualizations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The report is generated from public search results and should label price, sales, and ranking data as point-in-time estimates; the bundled template loads Chart.js from jsDelivr unless modified to be fully self-contained.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
