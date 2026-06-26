## Description: <br>
Hizal Write guides an agent to persist decisions, conventions, observations, identity notes, and org knowledge through dedicated Hizal write tools as it works. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkerscobey](https://clawhub.ai/user/parkerscobey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to keep durable memory of useful decisions, conventions, lessons, identity notes, and org knowledge while an agent works. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages automatic durable memory writes while an agent works. <br>
Mitigation: Require explicit save approval or a clear policy before using it, and default to narrow memory scopes. <br>
Risk: Sensitive or confidential information could be persisted in memory. <br>
Mitigation: Forbid storage of secrets, credentials, personal data, customer content, confidential code, and temporary reasoning notes unless deliberately approved. <br>
Risk: Broad project, agent, or org scopes and auto-injection can spread incorrect or private context. <br>
Mitigation: Review scope, source fields, and inject audience before writes, and keep principle promotion under human review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/parkerscobey/hizal-write) <br>
- [Publisher profile](https://clawhub.ai/user/parkerscobey) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code] <br>
**Output Format:** [Markdown with tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for writing durable memory chunks through Hizal tools; no generated files are described by the artifact.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
