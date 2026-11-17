## Description:

Model Router Hook routes OpenClaw interactions between fast and thinking Kimi models based on task complexity, intent signals, budget, and learned user preferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevinzhj](https://clawhub.ai/user/kevinzhj)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to choose between lower-cost fast responses and deeper thinking-model responses for coding, analysis, support, and other task-routing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change the active OpenClaw model session.

Mitigation: Review the routing policy and test model switching in a controlled session before enabling it for normal use.

Risk: The skill persists user profiles, session memory, and cost records under the user's home directory.

Mitigation: Use only with trusted publishers and confirm that local cross-session memory storage is acceptable for the deployment.

Risk: The artifact depends on an unbundled model_router_v3 module.

Mitigation: Verify and install the missing dependency from a trusted source before relying on the router.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kevinzhj/skills/model-router-hook)
- [Artifact source: SKILL.md](artifact/SKILL.md)
- [Artifact source: scripts/model_router.py](artifact/scripts/model_router.py)

## Skill Output:

**Output Type(s):** [Code, Configuration, Guidance]

**Output Format:** [Python API results and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns routing metadata such as selected mode, model, decision log, switch status, cost records, dashboard data, and health status.]

## Skill Version(s):

4.0.0 (source: server release metadata and artifact __version__)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
