## Description: <br>
Integrates with Moodle 4.x REST Web Services so an agent can create and duplicate courses, manage enrollments, create activities, update grades, list learners, and send internal messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[exeandino](https://clawhub.ai/user/exeandino) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Moodle administrators and developers use this skill to operate Moodle courses through Web Services REST, including course creation, enrollment changes, activity setup, grading, learner listing, and internal messaging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delete Moodle courses or categories through maintenance scripts. <br>
Mitigation: Review or remove deletion scripts before installation, run them only with explicit human confirmation, and keep current backups for production Moodle sites. <br>
Risk: Bulk messaging can contact many students from a trusted Moodle account. <br>
Mitigation: Limit token permissions, review message recipients and content before sending, and use the skill only from an administrator account authorized for student communications. <br>
Risk: The Moodle Web Service token can grant broad administrative access if exposed or over-scoped. <br>
Mitigation: Store the token outside Git, avoid displaying it in chat, regenerate it if exposed, and use the least privileges needed for the intended Moodle tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/exeandino/moodle-ws) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, code, API calls] <br>
**Output Format:** [Markdown guidance with inline command and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Moodle base URL and a least-privilege Web Service token stored outside Git.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
