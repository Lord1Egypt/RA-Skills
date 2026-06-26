## Description: <br>
Integrates with Moodle 4.x REST Web Services to create courses, manage enrollments, update activities, submit grades, and list courses or students. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[exeandino](https://clawhub.ai/user/exeandino) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, educators, and Moodle administrators use this skill to help an agent plan and carry out Moodle 4.x course, enrollment, activity, grade, and roster workflows through REST Web Services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to make real Moodle course, enrollment, activity, or grade changes. <br>
Mitigation: Require the agent to list and confirm exact Moodle changes before applying them, and test workflows in a non-production Moodle instance first. <br>
Risk: Moodle Web Service tokens can expose administrative capabilities if shared or over-scoped. <br>
Mitigation: Use a dedicated least-privilege token and keep the Moodle URL and token out of chat and version control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/exeandino/moodle-ws-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline code and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Moodle REST Web Services calls and configuration steps that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
