## Description: <br>
Provides Chinese-language oncology research reports that synthesize literature, epidemiology, clinical guidance, drug data, and trials for cancer treatment and drug-development questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patsnaplifescience](https://clawhub.ai/user/patsnaplifescience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External life-science and biopharma users use this skill to research cancer mechanisms, standards of care, epidemiology, clinical trials, and commercial feasibility for oncology drug-development decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a PatSnap API key for MCP service access. <br>
Mitigation: Install only when PatSnap MCP access is intended, keep API keys protected, and avoid embedding real keys in shared logs or examples. <br>
Risk: Oncology research outputs may influence medical or drug-development decisions. <br>
Mitigation: Verify conclusions against source documents and qualified medical or drug-development experts before acting on them. <br>
Risk: If the PatSnap MCP service is unavailable or unauthenticated, data retrieval can fail. <br>
Mitigation: Run the documented connectivity check before analysis and stop rather than continuing with incomplete MCP data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/patsnaplifescience/precision-oncology-zhcn) <br>
- [PatSnap Life Science](https://eureka.patsnap.com/ls-landing) <br>
- [PatSnap Developer Portal](https://open.patsnap.com/devportal) <br>
- [PatSnap Pharma Intelligence MCP Service](https://open.patsnap.com/marketplace/mcp-servers/096456) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with Roman-numeral sections and setup command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PatSnap Life Science MCP connection and an API key; reports must include a conclusion section and avoid unsupported medical claims.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence; artifact frontmatter lists 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
