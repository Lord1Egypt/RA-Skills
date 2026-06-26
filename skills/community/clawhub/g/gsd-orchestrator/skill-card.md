## Description: <br>
Orchestrate GSD projects through `gsd headless` subprocess execution for milestone creation, workflow execution, status polling, blocker handling, and cost tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[glittercowboy](https://clawhub.ai/user/glittercowboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to create and execute GSD milestones, inspect project state, parse structured run results, handle blockers, and monitor cost during software development workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents broad headless project-execution capability through GSD workflows. <br>
Mitigation: Install only for trusted repositories, prefer `query` and `next` before full `auto`, run on a branch or sandbox, and review `.gsd/` state plus code diffs. <br>
Risk: Answer files can inject secrets into the child process environment. <br>
Mitigation: Use short-lived least-privilege secrets, keep answer files out of version control, and verify secrets are not committed. <br>
Risk: The required `gsd` binary is installed from the `gsd-pi` Node package. <br>
Mitigation: Verify or pin the `gsd-pi` package before deployment. <br>


## Reference(s): <br>
- [GSD Commands Reference](references/commands.md) <br>
- [HeadlessJsonResult Reference](references/json-result.md) <br>
- [Answer Injection](references/answer-injection.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/glittercowboy/gsd-orchestrator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to emit plain text, structured JSON, or JSONL event streams through GSD command usage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
