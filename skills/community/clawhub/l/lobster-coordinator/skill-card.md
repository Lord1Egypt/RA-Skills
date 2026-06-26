## Description: <br>
Coordinates multi-agent work through single-task delegation, team collaboration, and global dispatch patterns for complex OpenClaw tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate complex tasks across sub-agents, parallel worker teams, shared scratchpads, progress summaries, and review stages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegated agents may receive broad authority with unclear activation and permission boundaries. <br>
Mitigation: Require explicit approval before entering Coordinator or Swarm mode, keep each worker tool list narrow, and ensure deny rules apply to child agents. <br>
Risk: Background sub-agent sessions and shared scratchpads can expose sensitive task data or make activity harder to monitor. <br>
Mitigation: Monitor background sessions, control scratchpad retention and access, and avoid sensitive data unless retention and access controls are understood. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wangxiaofei860208-source/lobster-coordinator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured coordination steps and inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May spawn and coordinate background sub-agent sessions when the host agent supports the required OpenClaw tools.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
