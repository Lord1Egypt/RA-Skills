## Description: <br>
Computer use for GUI automation tasks via VLA models. Use when the user describes a task in natural language that requires visual screen interaction and no API or CLI exists for the target app. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanningwang](https://clawhub.ai/user/hanningwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to run bounded desktop GUI automation tasks from natural-language instructions when an application lacks a suitable API or CLI path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control the visible desktop and may perform sensitive or irreversible actions during explicit user tasks. <br>
Mitigation: Supervise active sessions, use step limits and the stop control, and require explicit confirmation for purchases, credential entry, deletion, or account changes. <br>
Risk: Cloud mode may send primary-display screenshots and may use a shell helper for applicable steps. <br>
Mitigation: Prefer local mode for private screens and disable cloud shell use with `mano-cua config --set disable-bash true` when shell execution is not needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hanningwang/mano-cua) <br>
- [mano-cua source repository](https://github.com/Mininglamp-AI/mano-skill) <br>
- [mano-cua releases](https://github.com/Mininglamp-AI/mano-skill/releases) <br>
- [Mano-P model](https://huggingface.co/Mininglamp-2718/Mano-P) <br>
- [Cloud model network-call module](https://github.com/Mininglamp-AI/mano-skill/blob/main/visual/model/task_model.py) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include mano-cua CLI invocations, local-mode setup steps, and supervision guidance for GUI automation tasks.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
