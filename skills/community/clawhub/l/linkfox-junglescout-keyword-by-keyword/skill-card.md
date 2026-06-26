## Description: <br>
Expands a single Amazon seed keyword into related Jungle Scout keyword metrics, including search volume, trends, PPC bid data, ranking difficulty, and marketplace coverage for 10 Amazon sites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketplace operators and ecommerce analysts use this skill to expand Amazon seed keywords, find long-tail opportunities, compare PPC bid ranges, and assess competition metrics across supported marketplaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive LinkFox API key and sends Amazon keyword queries to a third-party service. <br>
Mitigation: Install only in environments where LINKFOXAGENT_API_KEY can be scoped and protected, and review whether the query data is acceptable to share with LinkFox. <br>
Risk: The artifact directs agents to send user feedback, intent, or business context to a separate LinkFox feedback endpoint without interrupting the user's flow. <br>
Mitigation: Require explicit user confirmation before using the feedback API path, or disable that path in deployments where silent feedback reporting is not allowed. <br>


## Reference(s): <br>
- [Jungle Scout Keyword by Keyword API Reference](references/api.md) <br>
- [ClawHub release page](https://clawhub.ai/linkfox-ai/linkfox-junglescout-keyword-by-keyword) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables and summaries, with optional JSON parameters or shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY; accepts one seed keyword per call; returns keyword metrics for supported Amazon marketplaces.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
