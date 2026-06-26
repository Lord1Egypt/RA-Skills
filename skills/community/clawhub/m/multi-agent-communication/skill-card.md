## Description: <br>
Based on two core tools, sessions_spawn and sessions_send, this skill helps users build, manage, and optimize distributed Agent systems for task decomposition, parallel processing, and efficient coordination among Agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to choose and configure multi-agent spawning, messaging, collaboration, and workflow patterns with sessions_spawn and sessions_send. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Background child agents and copied attachments can reduce user visibility or keep sensitive material available outside the parent agent lifecycle. <br>
Mitigation: Use visible session mode for sensitive work and do not pass sensitive attachments to child agents unless the copy and retention behavior is acceptable. <br>
Risk: Broad cross-agent permissions, high child-agent limits, or long-running tasks can increase coordination and resource-exhaustion risk. <br>
Mitigation: Prefer explicit allow lists, avoid allow-all communication settings, and keep recursion depth, child-agent limits, and timeouts conservative. <br>


## Reference(s): <br>
- [Agent Configuration Reference](references/config.md) <br>
- [Design Pattern Reference](references/patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/openlark/multi-agent-communication) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, code] <br>
**Output Format:** [Markdown with inline JSON5 and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sessions_spawn and sessions_send call patterns, workflow recommendations, and configuration examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
