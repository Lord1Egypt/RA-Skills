## Description: <br>
Analyze and improve the improvement process for agent skills by detecting regressions, extracting meta-patterns from prior outcomes, and recommending strategy adjustments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill after batches of skill improvements, regressions, or periodic review cycles to assess what worked and refine future improvement strategy. It helps summarize improvement outcomes, identify success and failure patterns, and propose changes for human approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local trace logging can retain tool targets, decision rationale, outcomes, and improvement patterns that may include sensitive project context. <br>
Mitigation: Use only in workspaces where trace logging is acceptable, and periodically review or delete ~/.claude/skills/traces/ and improvement_memory.json when sensitive context may have been captured. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-abstract-metacognitive-self-mod) <br>
- [Metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/abstract) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown report with recommendations, metrics, and inline code or shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May record meta-insights and trace-derived findings in local improvement memory when the workflow is followed.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
