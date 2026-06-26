## Description: <br>
Scores agent actions by expected gain, cost, uncertainty, and redundancy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to score whether an agent should respond, retrieve, call a tool, verify, delegate, or stop during multi-step orchestration. It helps gate expensive actions and record concise utility-based reasoning before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad triggers may cause the skill to appear in general decision-making contexts. <br>
Mitigation: Invoke it for multi-step orchestration, delegation, verification, or cost-control tasks where utility scoring is useful. <br>
Risk: Heuristic utility scores can produce misleading guidance when treated as definitive. <br>
Mitigation: Use advisory mode by default, document overrides, and reserve prescriptive gating for explicitly opted-in workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/athola/nm-leyline-utility) <br>
- [claude-night-market leyline plugin](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>
- [Utility-Guided Agent Orchestration for Efficient LLM Tool Use](https://arxiv.org/abs/2603.19896) <br>
- [State Builder](modules/state-builder.md) <br>
- [Action Selector](modules/action-selector.md) <br>
- [Integration](modules/integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with utility scores and action reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; no executable code or hidden data access.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
