## Description: <br>
Compact AI-to-AI communication protocol. Use when spawning sub-agents, sending inter-agent messages via sessions_send/sessions_spawn, or when instructed to speak OpenLang. Reduces token usage 5-10x on agent-to-agent channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andreanjos](https://clawhub.ai/user/andreanjos) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use OpenLang to write compact agent-to-agent task descriptions, session messages, and result announcements while keeping human-facing channels in normal language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compressed agent-to-agent messages could be mistaken for authorization to perform sensitive actions. <br>
Mitigation: Keep normal approval and policy checks in place before running commands, modifying files, accessing databases, using credentials, or performing destructive actions. <br>
Risk: Compact notation can omit nuance that would be clearer in normal language. <br>
Mitigation: Use normal language for human-facing channels and fall back to the less compressed L1 form when the grammar cannot clearly express the intended meaning. <br>


## Reference(s): <br>
- [OpenLang on ClawHub](https://clawhub.ai/andreanjos/openlang) <br>
- [andreanjos Publisher Profile](https://clawhub.ai/user/andreanjos) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance with protocol examples and compact text notation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces human-authored shorthand for agent-to-agent messages; it does not execute commands or grant authorization.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
