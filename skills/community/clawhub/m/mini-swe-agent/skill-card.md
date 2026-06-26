## Description: <br>
Autonomously run complex software engineering tasks like bug fixes or feature implementation using the mini-swe-agent CLI with full codebase edits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[c1nderscript](https://clawhub.ai/user/c1nderscript) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to delegate complex software engineering tasks, such as bug fixes, feature implementation, and GitHub issue resolution, to the mini-swe-agent CLI for end-to-end codebase exploration and editing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs an agent to run an external coding tool in autonomous no-confirmation mode that can inspect and edit a repository. <br>
Mitigation: Install only when that behavior is intended, verify the mini CLI source and version, run it in a disposable branch or sandbox, and review diffs and tests before keeping changes. <br>
Risk: Autonomous repository edits can introduce incorrect changes or be excessive for simple fixes. <br>
Mitigation: Use standard editing tools for minor replacements or typo fixes, and reserve this skill for complex engineering tasks that warrant end-to-end exploration. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and resulting repository changes from the external CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill instructs use of mini with --yolo for autonomous repository inspection and editing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
