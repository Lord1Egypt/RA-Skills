## Description: <br>
Combines academic literature, epidemiology reports, clinical and pharmaceutical guidance, and clinical trial reports to produce oncology treatment and drug-development reports with molecular biology and histology profiling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patsnaplifescience](https://clawhub.ai/user/patsnaplifescience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External pharmaceutical R&D and business development users use this skill to investigate cancer indications, standards of care, clinical trials, drug-development opportunities, unmet medical needs, epidemiology, and commercial viability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a PatSnap API key and sends oncology research queries to PatSnap LifeScience MCP services, which can expose sensitive credentials or confidential research context if mishandled. <br>
Mitigation: Use organization-approved secret handling, verify the PatSnap endpoint, rotate exposed keys, and avoid placing API keys in shared command history or logs. <br>
Risk: Queries may include patient identifiers, confidential clinical details, proprietary project names, or private R&D strategy. <br>
Mitigation: Do not submit protected health information or confidential R&D content unless the organization has approved sending it to PatSnap and any fallback search provider. <br>
Risk: Supplemental web search can introduce unverified or conflicting public information into oncology reports. <br>
Mitigation: Review cited sources and reconcile public-search results against approved clinical, regulatory, and internal sources before business or clinical use. <br>


## Reference(s): <br>
- [Precision Oncology on ClawHub](https://clawhub.ai/patsnaplifescience/precision-oncology) <br>
- [PatSnap Pharma Intelligence MCP Server](https://open.patsnap.com/marketplace/mcp-servers/096456) <br>
- [PatSnap Chemical Molecular MCP Server](https://open.patsnap.com/marketplace/mcp-servers/713886) <br>
- [PatSnap Biology Modality MCP Server](https://open.patsnap.com/marketplace/mcp-servers/06e741) <br>
- [PatSnap Life Science](https://eureka.patsnap.com/ls-landing) <br>
- [PatSnap Dev Portal](https://open.patsnap.com/devportal) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with structured sections and optional inline shell commands for setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PatSnap LifeScience MCP connectivity; web search may supplement MCP results only after MCP retrievals are complete or when current information is required.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
