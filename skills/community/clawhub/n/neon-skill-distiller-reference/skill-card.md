## Description: <br>
Complete skill compression documentation covering options, modes, and calibration details for reducing agent skill context usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to compress verbose skill documentation while preserving triggers, core instructions, constraints, and transparent trade-off reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private or proprietary skill text may be analyzed by the agent's configured LLM provider. <br>
Mitigation: Confirm the active provider and trust boundary before processing sensitive skill content. <br>
Risk: Local calibration history may record metadata about compression runs. <br>
Mitigation: Review or clear local calibration files before sharing workspaces or processing sensitive skills. <br>
Risk: Compressed skill output can omit details or introduce misleading guidance if accepted without review. <br>
Mitigation: Review and scan compressed skills before deployment, especially when using aggressive token targets. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/leegitw/neon-skill-distiller-reference) <br>
- [Project homepage](https://github.com/live-neon/skills/tree/main/skill-distiller/reference) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with optional code blocks, shell commands, and JSONL calibration metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include functionality-preservation estimates, token-reduction statistics, removed/kept section summaries, and local calibration metadata.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
