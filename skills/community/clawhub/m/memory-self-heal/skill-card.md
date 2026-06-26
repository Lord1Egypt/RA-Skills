## Description: <br>
General-purpose self-healing loop that learns from past failures, retries safely, and records reusable fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dalomeve](https://clawhub.ai/user/Dalomeve) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent repeats failures, stalls, or reports completion without a verifiable artifact. It guides the agent through evidence scanning, failure classification, bounded retries, safe fallback, controlled escalation, and concise memory writeback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may cause an agent to read workspace memory, task files, and logs while troubleshooting. <br>
Mitigation: Install only where that local evidence access is acceptable, and keep secrets out of memory, task, and log files. <br>
Risk: Recorded recovery notes could preserve sensitive details or incorrect fixes for later reuse. <br>
Mitigation: Review memory entries periodically and keep writebacks concise, omitting secrets, tokens, and unverified rules. <br>
Risk: Repeated automated retries can waste time or amplify a bad recovery path. <br>
Mitigation: Follow the documented maximum of three retries per blocker signature and escalate with the minimum unblock input when the issue remains unresolved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Dalomeve/memory-self-heal) <br>
- [Dalomeve publisher profile](https://clawhub.ai/user/Dalomeve) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown guidance with shell command examples and structured checklist/writeback blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only troubleshooting helper; no external API keys or MCP tools are declared in the evidence.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
