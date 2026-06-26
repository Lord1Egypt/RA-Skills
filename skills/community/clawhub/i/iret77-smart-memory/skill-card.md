## Description: <br>
Smart Memory sets up a five-layer memory architecture for OpenClaw agents to reduce context bloat, preserve active project knowledge, and support single-agent or multi-agent setups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iret77](https://clawhub.ai/user/iret77) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators of OpenClaw agents use this skill to organize long-running agent memory, keep active project context visible, and route project or agent-specific knowledge in single-agent and multi-agent setups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring session-history maintenance can rewrite internal OpenClaw session files, including an unsafe raw trim path. <br>
Mitigation: Review and likely remove or rewrite the automatic session-trimming section before installation; back up MEMORY.md, AGENTS.md, HEARTBEAT.md, memory/, and .openclaw session files first. <br>
Risk: Session trimming or repair can damage an active or incomplete tool-call exchange. <br>
Mitigation: Prefer a vetted boundary-aware trim tool with explicit user approval, and only repair stale session files that have not been modified for more than five minutes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iret77/iret77-smart-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown setup guidance with bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to create or update OpenClaw memory, agent, heartbeat, and session-maintenance files.] <br>

## Skill Version(s): <br>
1.5.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
