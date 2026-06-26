## Description: <br>
Queries Zhihuiya (PatSnap) for patent legal status, lifecycle status, and legal event history by patent ID or publication number. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Patent, IP, and legal workflow users use this skill to check whether patents are active, pending, inactive, expired, revoked, or associated with legal events such as transfer, license, pledge, opposition, litigation, or re-examination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Patent identifiers and related business or legal context may be sent to LinkFox/PatSnap during lookup. <br>
Mitigation: Treat patent queries as potentially confidential and get user approval before submitting sensitive identifiers or context. <br>
Risk: The skill documentation describes automatic feedback submission to a separate LinkFox feedback endpoint. <br>
Mitigation: Require explicit user approval before sending feedback content, intent details, or user sentiment outside the current conversation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-zhihuiya-legal-status) <br>
- [Zhihuiya Legal Status API Reference](artifact/references/api.md) <br>
- [Zhihuiya Legal Status API Endpoint](https://tool-gateway.linkfox.com/zhihuiya/legalStatus) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown summaries and tables, with JSON API results or shell command examples when needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY. Requests accept patentId or patentNumber, with comma-separated batches of up to 100 patent identifiers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
