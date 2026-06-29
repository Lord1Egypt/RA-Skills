## Description: <br>
Queries World Bank poverty and inequality data by country or region, including poverty headcounts, Gini index, income shares, trends, regional comparisons, and SDG context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and researchers use this skill to add AgentPMT-hosted queries for poverty, inequality, regional comparison, trend analysis, policy research, and SDG monitoring workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tool inputs are sent to AgentPMT-hosted infrastructure. <br>
Mitigation: Keep requests minimal and do not include secrets, private personal details, internal identifiers, wallet private keys, mnemonics, signatures, or payment headers unless explicitly intended for that service. <br>
Risk: Poverty and inequality indicators can be delayed or incomplete for some countries and metrics. <br>
Mitigation: Use returned source attribution, years, data notes, and availability warnings when interpreting results, especially for time-sensitive analysis. <br>


## Reference(s): <br>
- [AgentPMT Marketplace Product](https://www.agentpmt.com/marketplace/global-poverty-inequality-data) <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/global-poverty-inequality-data) <br>
- [Generated Action Schema](artifact/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JSON request and response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote AgentPMT tool calls return JSON poverty and inequality data, trends, regional comparisons, insights, SDG notes, and data notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
