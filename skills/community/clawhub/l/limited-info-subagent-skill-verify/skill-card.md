## Description: <br>
Validate whether a skill can be executed successfully by a minimally informed subagent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amourlion](https://clawhub.ai/user/amourlion) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to test whether another skill can be executed correctly when a subagent receives only a sparse invocation and a minimal artifact. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A subagent may exercise a target skill or artifact under intentionally sparse instructions. <br>
Mitigation: Use the skill only with target skills and artifacts that are appropriate for subagent testing, and disable implicit invocation when manual control is required. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown verdict with findings and improvement guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill reports pass or fail, explains any acceptance gaps, and suggests targeted skill improvements when needed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
