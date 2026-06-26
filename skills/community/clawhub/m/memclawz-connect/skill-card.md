## Description: <br>
Connects AI agents to the MemClawz shared memory bus with read-before-act and write-after-complete workflows over a simple HTTP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yoniassia](https://clawhub.ai/user/yoniassia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give agents shared memory across sessions and systems. Agents can search prior facts, decisions, procedures, and outcomes before work, then write useful results back after significant tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shared memory can persist sensitive information such as secrets, personal data, private prompts, customer data, security findings, or proprietary project details. <br>
Mitigation: Require explicit approval before storing sensitive entries, define retention expectations, and keep memory contents limited to information appropriate for shared agent context. <br>
Risk: A broad HTTP memory service can be exposed to unintended agents or network peers if deployed without authentication, HTTPS, and access controls. <br>
Mitigation: Keep the service on localhost or a trusted private network unless HTTPS, authentication, and access controls are configured. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yoniassia/memclawz-connect) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash, JSON, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses MEMCLAWZ_URL, MEMCLAWZ_AGENT_ID, and optional MEMCLAWZ_API_KEY environment variables.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
