## Description: <br>
Query Zhihuiya (PatSnap) patent cited-by data, including citation counts and citing patent details, by patent ID or publication number. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and patent analysts use this skill to look up forward citation counts, family citation metrics, and citing patent details for one or more patents. Agents can use it to prepare factual citation tables and comparisons without making valuation or investment judgments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Patent numbers, patent IDs, and the LinkFox API key are sent to LinkFox/PatSnap services during lookup. <br>
Mitigation: Use the skill only when sharing those identifiers with LinkFox/PatSnap is acceptable, and avoid confidential patent research unless approved. <br>
Risk: The artifact instructs the agent to report feedback and user context to a separate LinkFox feedback endpoint. <br>
Mitigation: Disable feedback reporting or require explicit user consent before sending comments, intent, or satisfaction context. <br>


## Reference(s): <br>
- [Zhihuiya Patent Cited API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-zhihuiya-cited-by) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples and optional shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Patent lookup requests require at least one patentId or patentNumber value and use LINKFOXAGENT_API_KEY for authenticated API access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
