## Description: <br>
Skill discovery engine. Analyzes what your agent does and recommends ClawHub skills you're missing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whooshinglander](https://clawhub.ai/user/whooshinglander) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to profile local agent workflows, find gaps in installed skills, and receive prioritized ClawHub skill recommendations with trust scores and install commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reviews local agent memory, logs, configuration, cron context, and installed skill files, which may contain sensitive operational context. <br>
Mitigation: Run it only in trusted local workspaces and keep outputs limited to summarized patterns; the artifact instructs credential and home-path redaction. <br>
Risk: Recommended skills may add capabilities such as network access, file writes, account actions, or credential handling after installation. <br>
Mitigation: Review each recommended skill, its ClawHub page, permissions, and security status before running the install command. <br>
Risk: The bundled catalogue can lag behind current ClawHub releases, and trust scores are heuristic. <br>
Mitigation: Refresh the catalogue when possible and treat scores as decision support rather than proof of safety or quality. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/whooshinglander/iknowkungfu) <br>
- [Workflow Analysis Procedure](references/workflow-analysis.md) <br>
- [Recommendation Engine Procedure](references/recommendation-engine.md) <br>
- [Trust Scoring Methodology](references/scoring.md) <br>
- [Security Quick Check](references/security-check.md) <br>
- [Skills Index Documentation](references/skills-index.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown-style workflow profile and recommendation report with trust scores, rationale, and install commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Top-five recommendations; summarizes patterns only and redacts credentials and username-bearing paths.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
