## Description: <br>
Linux real-time programming assistant. Generates, reviews, and modifies C code for periodic control tasks and interrupt-driven programs. Enforces RT scheduling, CPU isolation, clock_nanosleep loops, and threaded IRQ best practices. Only handles Linux RT programming topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xgkucas](https://clawhub.ai/user/xgkucas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate, review, or modify Linux real-time C programs for periodic control tasks and interrupt-driven workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Privileged Linux tuning commands can disrupt the user's machine, including graphical sessions, CPU frequency policy, power use, and thermal behavior. <br>
Mitigation: Use the skill on a dedicated or disposable Linux real-time test machine when possible, and confirm rollback steps before running commands such as sudo init 3 or all-core CPU governor changes. <br>
Risk: Generated real-time C code and root-level run commands may be unsafe if applied without review. <br>
Mitigation: Review generated C code and shell commands before compiling or running them with elevated privileges. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with C and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a C source attachment, build and run commands, and a Linux real-time system checklist.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
