## Description: <br>
Applies NASA Power of 10 rules for safety-critical verifiable code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and code reviewers use this skill to evaluate safety-critical, financial, medical, data-integrity, and other high-reliability code with adapted NASA Power of 10 guidance. It helps an agent recommend stricter control-flow, loop-bound, assertion, validation, scope, and linting practices while matching rigor to consequence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad triggers such as safety, medical, or high-reliability system code may activate the skill during unrelated work. <br>
Mitigation: Narrow triggers locally when broad activation is unwanted. <br>
Risk: Safety-critical guidance can be too strict for prototypes, scripts, or non-critical utilities. <br>
Mitigation: Apply the skill as advisory review guidance and match rigor to the consequence of the code being reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-pensive-safety-critical-patterns) <br>
- [Publisher profile](https://clawhub.ai/user/athola) <br>
- [Metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/pensive) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with code, shell command, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; the skill does not request runtime access or perform actions.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
