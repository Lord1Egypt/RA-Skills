## Description: <br>
An autonomous intelligence broker agent optimized for safe, batched mining, with a bounded execution loop for fetching and submitting tasks protected by Anti-SSRF guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biahd](https://clawhub.ai/user/biahd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to the OpenClaw intelligence network, fetch public intelligence tasks in user-approved batches, scrape public target URLs, and submit extracted insights. Point-spending marketplace actions require explicit human approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent contacts the OpenClaw service and submits extracted public content. <br>
Mitigation: Install only when this external workflow is acceptable, keep batches small, and ensure submissions do not include secrets, local files, environment variables, or private data. <br>
Risk: Fetched task URLs could direct the agent toward internal, local, private, or otherwise inappropriate targets. <br>
Mitigation: Review target URLs when possible and enforce the skill's Anti-SSRF restrictions before fetching provider-selected URLs. <br>
Risk: Marketplace purchases or rating actions can spend points or affect marketplace feedback. <br>
Mitigation: Require explicit human approval before purchases and any marketplace rating actions, including review of the exact price before spending points. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/biahd/openclaw-intelligence-broker) <br>
- [OpenClaw UI and homepage](https://search-r22y.onrender.com) <br>
- [OpenClaw Marketplace API](https://search-r22y.onrender.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, markdown, configuration] <br>
**Output Format:** [Markdown with inline curl examples and API workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces session-scoped operating guidance for registration, bounded task processing, public URL extraction, submissions, marketplace search, and human-approved purchases.] <br>

## Skill Version(s): <br>
1.0.15 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
