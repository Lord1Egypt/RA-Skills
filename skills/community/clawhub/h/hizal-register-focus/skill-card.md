## Description: <br>
Declares the agent's current task and focus tags so matching context chunks can be injected into the active session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkerscobey](https://clawhub.ai/user/parkerscobey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to register the current task and focused tags at session start, after a reset, or when work changes. It helps route matching context into the active session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad self-trigger wording may cause the agent to update focus during ordinary planning language and pull irrelevant context. <br>
Mitigation: Use specific, domain-relevant tags and re-register focus only when the task is clear or has changed significantly. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls] <br>
**Output Format:** [Markdown guidance with a structured focus-registration call] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires session_id, task, and tags; re-registering replaces the previous focus.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
