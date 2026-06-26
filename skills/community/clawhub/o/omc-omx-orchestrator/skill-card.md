## Description: <br>
异步派发编码任务到 OMC (claude -p) 或 OMX (omx exec)。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiuscut](https://clawhub.ai/user/qiuscut) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to dispatch local coding, analysis, review, and refactoring work to Claude Code or Codex CLI as background tasks. It helps create task specifications, launch detached jobs, track status, and recover task state after agent restarts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Background Claude/Codex jobs may run with broad local authority against project files. <br>
Mitigation: Use the skill only for intentional local coding jobs, choose trusted working directories, and review generated task specs and commands before launch. <br>
Risk: Prompts, specs, logs, or results may contain secrets or private customer data. <br>
Mitigation: Avoid placing sensitive data in task descriptions or generated specs, and monitor task folders that store result and log files. <br>
Risk: Detached processes can continue after the controlling agent restarts. <br>
Mitigation: Monitor task folders and PIDs, and use the provided recovery workflow to reconcile task status after restarts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/qiuscut/omc-omx-orchestrator) <br>
- [Recovery Guide](references/recovery-guide.md) <br>
- [Spec Template](references/spec-template.md) <br>
- [Task Schema](references/task-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON task metadata and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local task files such as task.json, spec.md, result.txt, log.txt, and exit_code when used by an agent.] <br>

## Skill Version(s): <br>
4.3.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
