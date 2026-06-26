## Description: <br>
Generates a step-by-step plan to fix a GitHub issue based on its title and description. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JINJIN2024UX](https://clawhub.ai/user/JINJIN2024UX) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, open source contributors, and bounty hunters use this skill to turn a GitHub issue title and description into a step-by-step fix plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Issue descriptions are echoed into the generated plan, so secrets, private vulnerability details, or confidential project information entered as input may appear in the output. <br>
Mitigation: Use public or non-sensitive issue text, and redact secrets or confidential details before running the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/JINJIN2024UX/github-bounty-radar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [String containing a Markdown-style issue fix plan] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes the submitted issue title and description in the returned plan.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
