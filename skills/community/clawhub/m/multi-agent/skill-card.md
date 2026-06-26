## Description: <br>
Production-ready multi-agent orchestration system for OpenClaw that implements Coordinator Mode with real parallel worker spawning, XML task notifications, state persistence, and a four-phase Research, Synthesis, Implementation, and Verification workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michealxie001](https://clawhub.ai/user/michealxie001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to coordinate complex OpenClaw coding tasks by preparing specialized worker agents, collecting XML task notifications, synthesizing findings, and producing implementation or verification work across parallel sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spawned worker agents may edit files, run commands, use web tools, and persist task data with broad workspace authority. <br>
Mitigation: Install only in workspaces where that authority is acceptable, review generated prompts before spawning workers, and keep implementation worker output under manual review. <br>
Risk: Task descriptions, prompts, notifications, and worker results may expose sensitive project context through spawned sessions or scratchpad files. <br>
Mitigation: Avoid including secrets in task text or context, and clean up kept sessions plus .openclaw scratchpad files after use. <br>


## Reference(s): <br>
- [Architecture Design](references/ARCHITECTURE.md) <br>
- [Test Report](test-report-phase2.5.md) <br>
- [Claude Code Coordinator Mode](https://zread.ai/instructkr/claude-code/19-coordinator-mode) <br>
- [ClawHub Skill Page](https://clawhub.ai/michealxie001/multi-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text instructions with shell commands, XML notification examples, generated worker prompt files, JSON worker state, and synthesized specification files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates .openclaw scratchpad files for worker state, prompts, results, and specifications.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
