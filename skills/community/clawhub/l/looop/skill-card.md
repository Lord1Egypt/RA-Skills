## Description: <br>
Claude Automated Development Toolkit - Decompose requirements documents, single files, or inline text into detailed task lists and automatically execute in loops until project completion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caesargattuso](https://clawhub.ai/user/caesargattuso) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn requirements documents, a single requirements file, or inline requirements into a task list and then run those tasks through Claude CLI against a source directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates Claude CLI with permission checks disabled and limited approval checkpoints. <br>
Mitigation: Install only for trusted repositories and requirements, and run on a disposable branch or copy before using results in production work. <br>
Risk: The skill can automatically edit files and commit changes, with optional remote push behavior. <br>
Mitigation: Use --max-tasks to limit each run, avoid --push until after manual review, and inspect diffs before relying on or sharing the result. <br>
Risk: Task logs may contain complete Claude CLI output, debug information, and project context from the run. <br>
Mitigation: Review .looop logs before sharing them and avoid running the skill on secrets or proprietary content unless that exposure is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caesargattuso/looop) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions, JSON task files, progress text, log files, git commits, and console output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores task state and logs under <src_dir>/.looop/ and can optionally push committed changes when --push is used.] <br>

## Skill Version(s): <br>
1.1.1 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
