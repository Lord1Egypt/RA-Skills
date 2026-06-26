## Description: <br>
Routes OpenClaw tasks between fast and thinking models based on task complexity, cost budget, and learned user preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevinZhj](https://clawhub.ai/user/kevinZhj) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to add local model-routing logic that chooses between lower-cost fast responses and deeper thinking responses for OpenClaw workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store user profile, session memory, and cost records locally. <br>
Mitigation: Use it only where local storage is acceptable, and review or periodically delete files under ~/.openclaw/workspace/memory/model-router/. <br>
Risk: Automatic model switching can affect response cost and behavior. <br>
Mitigation: Set an appropriate daily budget and verify the expected OpenClaw CLI or API model-switching behavior in the target environment. <br>


## Reference(s): <br>
- [Model router implementation](scripts/model_router.py) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Configuration, Guidance] <br>
**Output Format:** [Python module guidance with JSON-like routing results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local routing memory and cost records under ~/.openclaw/workspace/memory/model-router/ when used.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release metadata and __init__.py) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
