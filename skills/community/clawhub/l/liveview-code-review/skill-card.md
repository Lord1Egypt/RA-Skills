## Description: <br>
Reviews Phoenix LiveView code for lifecycle patterns, assigns/streams usage, components, and security. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Phoenix LiveView modules, HEEx templates, and LiveComponents for lifecycle, state-management, component, and security issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill references an adjacent review-verification protocol that may not be present in every agent environment. <br>
Mitigation: Inspect that protocol separately when available, or instruct the agent to rely only on this skill's included materials. <br>


## Reference(s): <br>
- [LiveView lifecycle reference](references/lifecycle.md) <br>
- [Assigns and streams reference](references/assigns-streams.md) <br>
- [LiveView components reference](references/components.md) <br>
- [LiveView security reference](references/security.md) <br>
- [ClawHub skill page](https://clawhub.ai/anderskev/liveview-code-review) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code review findings] <br>
**Output Format:** [Markdown review findings with file and line anchors] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are expected to use the [FILE:LINE] ISSUE_TITLE format and pass the skill's evidence, verification, line-anchor, and valid-pattern gates.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
