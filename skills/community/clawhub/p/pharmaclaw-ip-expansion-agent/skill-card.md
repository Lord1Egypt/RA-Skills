## Description: <br>
An intellectual property expansion agent for pharma drug discovery and development teams that analyzes molecules, patent references, and portfolio data to support infringement, freedom-to-operate, prior-art, novelty, and claim-strategy workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Cheminem](https://clawhub.ai/user/Cheminem) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Pharma IP, discovery, and portfolio teams use this skill to turn SMILES strings, therapeutic context, and patent/portfolio records into structured infringement, freedom-to-operate, novelty, and strategic claim recommendations. It is suited for agent workflows that need concise JSON or Markdown reports and generated molecular visualizations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External patent and compound lookups may expose confidential SMILES, targets, therapeutic strategy, or portfolio context. <br>
Mitigation: Run the skill only in controlled project directories and avoid third-party lookups unless organizational policy permits sharing that data. <br>
Risk: Generated local files such as ip_portfolio.db, logs/ip_expansion.log, ip_report.md, and ip_viz.png may contain sensitive portfolio or molecule information. <br>
Mitigation: Store generated files in approved locations, protect access to them, and remove or archive them according to the organization's data-handling rules. <br>
Risk: Cron-style portfolio monitoring can repeatedly process or disclose sensitive portfolio data if enabled unintentionally. <br>
Mitigation: Enable scheduled monitoring only with explicit operational intent and review the configured inputs, outputs, and retention settings first. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Cheminem/pharmaclaw-ip-expansion-agent) <br>
- [Publisher Profile](https://clawhub.ai/user/Cheminem) <br>
- [Patent/Compound APIs](references/apis.md) <br>
- [USPTO API Catalog](https://developer.uspto.gov/api-catalog) <br>
- [EPO Open Patent Services](https://developers.epo.org/) <br>
- [PubChem PUG REST](https://pubchem.ncbi.nlm.nih.gov/rest/pug) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Structured JSON and Markdown reports with generated PNG or SVG molecular visualizations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local portfolio database, report, visualization, and log files when the bundled scripts are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
