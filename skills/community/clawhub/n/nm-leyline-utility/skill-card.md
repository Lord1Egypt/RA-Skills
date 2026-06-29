## Description: <br>
Scores agent actions by expected gain, cost, uncertainty, and redundancy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to decide whether an agent should respond, retrieve, call a tool, verify, delegate, or stop based on utility scoring. It is useful for cost-aware orchestration, verification gating, model-tier selection, and limiting redundant agent actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad triggers such as orchestration, cost-control, and decision-making may cause the skill to appear in more workflows than a narrowly scoped skill. <br>
Mitigation: Install it only where agents should use a utility-scoring checklist for action selection. <br>
Risk: Prescriptive mode can change orchestration behavior by making the selected utility-scored action mandatory. <br>
Mitigation: Keep advisory mode as the default and enable prescriptive gating only through explicit consuming-skill frontmatter. <br>
Risk: Utility scoring is heuristic and may overvalue or undervalue actions when evidence, uncertainty, or redundancy estimates are poorly calibrated. <br>
Mitigation: Log the selected action, utility score, score breakdown, and any high-gain override before executing the action. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/athola/skills/nm-leyline-utility) <br>
- [Project Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>
- [State Builder](modules/state-builder.md) <br>
- [Action Selector](modules/action-selector.md) <br>
- [Integration](modules/integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with action report templates and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory by default; prescriptive utility gating is opt-in through consuming skill frontmatter.] <br>

## Skill Version(s): <br>
1.9.13 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
