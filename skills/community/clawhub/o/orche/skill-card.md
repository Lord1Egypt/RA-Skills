## Description: <br>
A multi-agent orchestration engine that executes complex tasks through Query, Plan, Execute, and Verify phases with phase gates, critic debate, hallucination checks, and verification-driven rework. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reikys](https://clawhub.ai/user/reikys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use Orche to coordinate complex, multi-step agent work that benefits from requirement clarification, debated planning, parallel execution, and independent verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous multi-agent execution can increase cost or perform broad work after initial approval. <br>
Mitigation: Set budget and concurrency limits, and request approval at each step for costly, external, or destructive tasks. <br>
Risk: Sensitive information included in prompts can be propagated into spawned agent work or local run records. <br>
Mitigation: Avoid putting secrets in prompts and review generated workspace files before sharing or committing them. <br>
Risk: Auto-proceeding after planning can continue execution before a user has reviewed the plan. <br>
Mitigation: Ask for explicit approval checkpoints when task scope, cost, external effects, or destructiveness matter. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/reikys/orche) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured plans, task files, verification reports, JSON state, and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create local orchestration state, phase deliverables, task outputs, verification reports, and completion summaries.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
