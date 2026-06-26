## Description: <br>
Routes each request to the best execution path: direct answer, installed skill, new skill, or a multi-skill workflow, with explicit reasoning about friction, value, and fit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ToBeWin](https://clawhub.ai/user/ToBeWin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to decide whether a request should be handled directly, by an installed skill, by a new skill, or by a multi-skill workflow. It is useful when the best execution path is uncertain and the agent should weigh value, friction, fit, and safety before recommending extra tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may recommend using or adding other skills, which can introduce separate security, privacy, or permission risks. <br>
Mitigation: Review any recommended skill separately before use, especially when it requests credentials, local data access, automation, or account permissions. <br>
Risk: Routing guidance could send a user toward unnecessary or unsuitable tooling if the request context is misunderstood. <br>
Mitigation: Check the stated route, confidence, and comparison against alternatives before acting on the recommendation. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text] <br>
**Output Format:** [Markdown route recommendation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes one primary route, confidence, next step, route comparison, and optional skill path when useful.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and metadata.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
