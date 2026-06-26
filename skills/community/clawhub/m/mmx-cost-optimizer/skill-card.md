## Description: <br>
MMX Cost Optimizer helps agents manage token budgets, monitor multi-dimensional AI usage costs, detect diminishing returns, and generate cost optimization guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[e2e5g](https://clawhub.ai/user/e2e5g) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to track token consumption, estimate AI costs, apply budget thresholds, and produce practical optimization suggestions for cost-sensitive agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session cost tracking can retain usage metrics that may be sensitive in some projects. <br>
Mitigation: Confirm the runtime limits this skill's hook and project-configuration access to its own cost and session data, and review retained metrics before using it in sensitive sessions. <br>
Risk: Cost optimization recommendations may over-prioritize savings compared with task quality or completeness. <br>
Mitigation: Review suggested budget thresholds and stop/continue decisions before applying them to important workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/e2e5g/mmx-cost-optimizer) <br>
- [Publisher profile](https://clawhub.ai/user/e2e5g) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with TypeScript examples, configuration snippets, cost reports, and optimization recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include token budget decisions, cost summaries, threshold settings, and session cost recovery guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
