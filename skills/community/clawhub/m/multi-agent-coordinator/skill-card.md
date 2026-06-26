## Description: <br>
Coordinates multiple child agents, such as Learner and Critic agents, to divide work, exchange results, and synthesize outcomes for complex tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangchunwanwusheng](https://clawhub.ai/user/yangchunwanwusheng) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate sub-agents for information gathering, quality review, and result integration when a single agent needs structured support for complex tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegated tasks may expose task details to child agents or shared memory. <br>
Mitigation: Avoid including credentials, private files, or sensitive personal data in delegated prompts or shared memory. <br>
Risk: Sub-agent outputs may be incomplete, stale, or lower quality than expected when one-shot agents time out or cannot persist context. <br>
Mitigation: Keep delegated prompts narrow, review returned results before synthesis, and use a Critic-style review step for important decisions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with JavaScript-style coordination examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no executable install behavior is disclosed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
