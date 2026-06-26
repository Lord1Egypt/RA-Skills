## Description: <br>
Manages OpenClaw agent and skill lifecycle tasks inside ClawForge, including classification, validation, publishing, installation, updates, deprecation, and retirement with a required local SSOT review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[felix-antonio-sl](https://clawhub.ai/user/felix-antonio-sl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and report OpenClaw agent or skill lifecycle changes in ClawForge, including routing to the next skill or command, blockers, risks, and rollback steps after SSOT preflight. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may propose high-impact publish, install, deploy, deprecate, retire, or artifact-write actions. <br>
Mitigation: Review generated lifecycle actions before allowing them, and require the documented SSOT preflight and rollback plan before changes proceed. <br>
Risk: Lifecycle guidance depends on local OpenClaw SSOT manuals being available and trusted. <br>
Mitigation: Verify the referenced local SSOT manuals are readable and trusted before accepting an output with ssot_reviewed marked true. <br>


## Reference(s): <br>
- [OpenClaw Lifecycle Manager release page](https://clawhub.ai/felix-antonio-sl/openclaw-lifecycle-manager) <br>
- [Publisher profile](https://clawhub.ai/user/felix-antonio-sl) <br>
- [SSOT Preflight](references/ssot-preflight.md) <br>
- [Agent Lifecycle Matrix](references/agent-lifecycle-matrix.md) <br>
- [Skill Lifecycle Matrix](references/skill-lifecycle-matrix.md) <br>
- [Internal Routing Map](references/internal-routing-map.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or YAML-style lifecycle report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes lifecycle state, preconditions, OpenClaw invariants, next action, blockers, risks, and rollback guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
