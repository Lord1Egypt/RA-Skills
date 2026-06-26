## Description: <br>
Enables communication between multiple Kiro instances by sharing and updating messages in a common chat file for coordinated interaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sonerbo](https://clawhub.ai/user/sonerbo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators who run multiple Kiro instances use this skill to coordinate short messages through a shared memory/kiro-chat.md file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages written to memory/kiro-chat.md persist and can be read by other instances or users with file access. <br>
Mitigation: Avoid secrets, tokens, private personal data, and high-impact instructions in the shared chat file; verify important requests before acting. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sonerbo/kiro-intercom) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown chat entries appended to a shared file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Messages persist in memory/kiro-chat.md and may be read by other Kiro instances with file access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
