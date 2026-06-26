## Description: <br>
This skill helps developers dispatch specialized agents for independent tasks that can be worked on without shared state or sequential dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to split unrelated debugging, testing, or subsystem work across focused parallel agents, then review and integrate the returned changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Parallel agents can interfere with each other when work is not truly independent or when they edit shared files or resources. <br>
Mitigation: Use narrow, independent scopes, avoid shared state, review returned changes for conflicts, and run the full relevant test suite before merging. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangxiaofei860208-source/lobster-dispatching-parallel-agents) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with example agent prompts and task dispatch calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces coordination guidance only; no executable payload.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
