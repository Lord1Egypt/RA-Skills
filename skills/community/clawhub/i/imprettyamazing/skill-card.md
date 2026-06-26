## Description: <br>
Interact with I'm Pretty Amazing (imprettyamazing.com), a platform for tracking and celebrating accomplishments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MacksMind](https://clawhub.ai/user/MacksMind) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to interact with an I'm Pretty Amazing account, including posting wins, tracking achievements, managing profile data, commenting, liking, following users, and submitting feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may handle sensitive login cookies and session tokens for an I'm Pretty Amazing account. <br>
Mitigation: Install only if account access is acceptable, decline saved session tokens on shared or synced machines, clear tokens when done, and avoid exposing token values in chat or logs. <br>
Risk: The skill can perform state-changing account actions such as posting, deleting, following, blocking, liking, commenting, profile updates, and feedback submission. <br>
Mitigation: Review the exact content, visibility, and account action before approving any mutation. <br>


## Reference(s): <br>
- [I'm Pretty Amazing skill page](https://clawhub.ai/MacksMind/imprettyamazing) <br>
- [I'm Pretty Amazing](https://imprettyamazing.com) <br>
- [I'm Pretty Amazing API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce authenticated API requests and session-token handling instructions when the user authorizes account access.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
