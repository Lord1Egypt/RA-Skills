## Description: <br>
Runs multiple independent tasks simultaneously by routing each to an appropriate AI model tier for faster parallel execution and combined results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nerua1](https://clawhub.ai/user/nerua1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to split independent repository tasks across parallel agent runs, collect their results, and optionally run lightweight build or test verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can launch multiple autonomous agents that may make overlapping repository changes. <br>
Mitigation: Use it on trusted repositories, preferably from a clean branch or disposable worktree, and keep task scopes narrow and non-overlapping. <br>
Risk: Task prompts and repository context may be sent to selected model backends. <br>
Mitigation: Avoid prompts containing secrets or proprietary material unless that exposure is approved for the model provider. <br>
Risk: Verification may run project build or test scripts in the target repository. <br>
Mitigation: Inspect package scripts before allowing verification to run and review generated changes before merging. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nerua1/nerua1-ultrawork) <br>
- [Ultrawork repository](https://github.com/nerua1/ultrawork) <br>
- [Ultrawork issues](https://github.com/nerua1/ultrawork/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style task summaries with shell command examples and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Aggregates parallel task results and may report build or test verification status.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
