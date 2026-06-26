## Description: <br>
Issue Register creates standardized WizNote issue-registration notes for a project and maintains an issue overview. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangfengxiang](https://clawhub.ai/user/wangfengxiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teams using WizNote can use this skill to capture project issues in a consistent note format, track status and severity, and keep an overview note synchronized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write to WizNote on the user's behalf, so an incomplete or incorrect configuration could place notes in the wrong project area. <br>
Mitigation: Fill and verify config.md before use, especially the project name, category path, and overview docGuid. <br>
Risk: Overview updates may include unrelated issue notes when multiple projects use similar issue-note titles. <br>
Mitigation: Narrow the search and update process for the intended project, or manually review the generated overview before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangfengxiang/issue-register) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, API calls] <br>
**Output Format:** [Markdown issue notes and overview updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured project name, category path, and overview docGuid in config.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
