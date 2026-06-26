## Description: <br>
Extract completed work into reusable AgentSkills and ask the user after complex task completion whether to generate a skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeremycooper2077](https://clawhub.ai/user/jeremycooper2077) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to recognize when completed work should be captured as a reusable AgentSkill and to guide creation of a focused SKILL.md plus supporting references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is proactive and may suggest updates to local skills that influence future agent behavior. <br>
Mitigation: Review the target path and full proposed diff before approving any durable write. <br>
Risk: Generated skill guidance can preserve incorrect or over-specific lessons from a completed task. <br>
Mitigation: Validate the proposed SKILL.md content and scan the skill before using it in future workflows. <br>


## Reference(s): <br>
- [Skill Template](references/skill-template.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jeremycooper2077/jc-skill-generator) <br>
- [Publisher Profile](https://clawhub.ai/user/jeremycooper2077) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with optional file paths, code blocks, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose durable local skill-file changes after user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
