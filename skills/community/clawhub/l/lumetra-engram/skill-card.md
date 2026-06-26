## Description: <br>
Persistent, explainable memory for your OpenClaw agent: store facts and recall them later via Lumetra's hosted Engram MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brutus-gr](https://clawhub.ai/user/brutus-gr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect an OpenClaw agent to Lumetra Engram so the agent can store durable memories, query prior context, list or delete memories, and cite recall traces when explaining remembered information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist selected user context to Lumetra's hosted Engram service. <br>
Mitigation: Configure it only when users are comfortable sending selected memories to that service, and prefer explicit approval before storing sensitive or long-lived memories. <br>
Risk: The skill requires an ENGRAM_API_KEY credential. <br>
Mitigation: Protect the API key, avoid exposing it in logs or shared configuration, and rotate it if disclosure is suspected. <br>
Risk: Stored memories may include personal, confidential, customer, health, financial, or credential-like information. <br>
Mitigation: Review memory content before storage and avoid persisting sensitive data unless the user has approved that use. <br>


## Reference(s): <br>
- [Lumetra homepage](https://lumetra.io) <br>
- [Lumetra model configuration](https://lumetra.io/models) <br>
- [ClawHub skill page](https://clawhub.ai/brutus-gr/lumetra-engram) <br>
- [Publisher profile](https://clawhub.ai/user/brutus-gr) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and MCP tool selectors] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter and ENGRAM_API_KEY; Engram tool calls may return JSON memory, bucket, deletion, or recall results.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
