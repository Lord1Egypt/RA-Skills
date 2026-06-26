## Description: <br>
Execute multiple tasks in parallel with timeout protection, error isolation, and real-time progress feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiukui666](https://clawhub.ai/user/qiukui666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run independent tasks concurrently, with per-task timeout controls, status reporting, and isolated failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start multiple local Hermes agent sessions at once. <br>
Mitigation: Use explicit, trusted task lists and avoid account-changing or destructive operations unless each task has been reviewed. <br>
Risk: Concurrent tasks can write to shared files or shared state at the same time. <br>
Mitigation: Avoid concurrent writes to shared files unless the task boundaries and ordering have been reviewed carefully. <br>
Risk: Task text handling may allow task content to affect spawned Hermes CLI options. <br>
Mitigation: Keep task descriptions trusted and update the executor to pass Hermes arguments as a structured array rather than building and splitting a command string. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qiukui666/openclaw-skill-parallel-tasks) <br>
- [OpenClaw repository](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal progress text, Markdown examples, and optional JSON task parsing output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes task status, duration, timeout, failure summaries, and exit codes.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
