## Description: <br>
Sets up and manages a long-running agent harness for complex, multi-session coding projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kzac313](https://clawhub.ai/user/kzac313) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Jumpstart to structure substantial coding projects into design documents, generated feature lists, progress logs, checkpoints, and repeatable implementation sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow directs an agent to actively modify project files, run local scripts, and make git commits. <br>
Mitigation: Use it on a clean branch or disposable workspace, inspect generated files, and review git status before relying on commits. <br>
Risk: The generated init.sh script may execute project-local commands during smoke testing. <br>
Mitigation: Review init.sh before execution and keep secrets out of the repository. <br>
Risk: Batch sessions can make multiple changes before stopping when jumploop is used. <br>
Mitigation: Start with small jumploop --n values and use checkpoint reviews before continuing through major milestones. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kzac313/jumpstart) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON file schemas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to create or update project files, run a local smoke-test script, and make git commits.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
