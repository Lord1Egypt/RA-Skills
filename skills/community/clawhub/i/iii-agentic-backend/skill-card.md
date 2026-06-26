## Description: <br>
Creates and orchestrates multi-agent pipelines on the iii engine for agent collaboration, orchestration, research/review/synthesis chains, and workflows where specialized agents hand off work through queues and shared state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rohitg00](https://clawhub.ai/user/rohitg00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design iii engine multi-agent workflows with named queues, shared state, approval gates, HTTP triggers, and pubsub completion events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shared agent state can expose sensitive data if secrets or unnecessary user data are stored there. <br>
Mitigation: Keep shared state free of secrets unless explicitly required, and limit stored data to what downstream agents need. <br>
Risk: Worker URLs, queue retries, approval gates, and downstream API permissions can create operational or access-control risk in production workflows. <br>
Mitigation: Apply normal production controls around worker endpoints, retry policies, explicit approvals, and API permissions before deployment. <br>
Risk: Reference code adapted from the skill may introduce application-specific issues outside the scanned artifact. <br>
Mitigation: Review and scan any iii reference code or workflow implementation separately before use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no executable code is shipped in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
