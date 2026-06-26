## Description: <br>
Route each user request to the most cost-effective model or multi-model workflow based on task type, complexity, risk, latency, budget, tool needs, and verification requirements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stephensu66](https://clawhub.ai/user/stephensu66) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to choose cost-effective model tiers, workflow shapes, and verification strategies for agent requests without overusing premium models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can influence which model or workflow handles future requests, so unsuitable routing could reduce answer quality or verification for sensitive tasks. <br>
Mitigation: Use it where cost-aware routing is desired, preserve its high-risk and exactness verification rules, and review routing recommendations before relying on them for material decisions. <br>


## Reference(s): <br>
- [Model Routing Orchestrator on ClawHub](https://clawhub.ai/stephensu66/model-routing-orchestrator) <br>
- [stephensu66 ClawHub profile](https://clawhub.ai/user/stephensu66) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text] <br>
**Output Format:** [Structured Markdown routing decision with task profile, execution plan, model role assignment, cost rationale, escalation rule, and fallback rule.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; no code execution, credential access, persistence, or hidden behavior was identified in the security evidence.] <br>

## Skill Version(s): <br>
2026.3.27 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
