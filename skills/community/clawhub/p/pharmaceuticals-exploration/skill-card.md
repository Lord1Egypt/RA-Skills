## Description: <br>
Answers drug-related questions by using PatSnap LifeScience services to retrieve and summarize patents, literature, drug records, clinical trials, safety data, and licensing transactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patsnaplifescience](https://clawhub.ai/user/patsnaplifescience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and life-science teams use this skill to investigate drugs, targets, diseases, clinical progress, competitive landscapes, pharmacovigilance, patents, literature, and licensing activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The PatSnap API key may be exposed through shell history or MCP configuration. <br>
Mitigation: Use a dedicated or least-privilege API key where available and avoid sharing command history or MCP configuration files. <br>
Risk: Drug research prompts and retrieved context may be processed by external PatSnap services. <br>
Mitigation: Submit confidential research data only when organizational policy permits PatSnap processing. <br>
Risk: Medical, safety, and pharmacovigilance outputs could be mistaken for clinical advice. <br>
Mitigation: Use outputs as research support and require qualified expert review before clinical, regulatory, or investment decisions. <br>
Risk: The skill depends on external MCP service connectivity and valid credentials. <br>
Mitigation: Verify MCP connectivity before use and stop troubleshooting after the first connection or authentication failure until configuration is corrected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/patsnaplifescience/pharmaceuticals-exploration) <br>
- [PatSnap Life Science](https://eureka.patsnap.com/ls-landing) <br>
- [PatSnap Dev Portal](https://open.patsnap.com/devportal) <br>
- [Pharma Intelligence MCP Server](https://open.patsnap.com/marketplace/mcp-servers/096456) <br>
- [Chemical Molecular MCP Server](https://open.patsnap.com/marketplace/mcp-servers/713886) <br>
- [Biology Modality MCP Server](https://open.patsnap.com/marketplace/mcp-servers/06e741) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown reports with tables and inline shell commands for setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PatSnap LifeScience MCP services and an API key; medical and drug-safety outputs should be treated as research support, not clinical advice.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
