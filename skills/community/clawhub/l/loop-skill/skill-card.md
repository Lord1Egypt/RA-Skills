## Description: <br>
Loop Skill helps an agent plan, launch, and manage unattended multi-repository coding-agent loops from written advancement plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[handsomestwei](https://clawhub.ai/user/handsomestwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill when they want an agent to scan one or more repositories, create or update advancement plans, dispatch coding-agent CLI work, and keep a recoverable background loop with dashboard monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended multi-repository automation may read broad workspace contents, write planning files, and start persistent background loops with too little confirmation or scoping. <br>
Mitigation: Use a specific project root, review the repositories discovered by scan, inspect generated or updated plans before relying on them, and be ready to stop the loop with the documented down command. <br>
Risk: The skill can dispatch coding-agent CLI work across multiple repositories, which may cause unintended changes if the target scope is too broad. <br>
Mitigation: Limit execution to intended repositories, avoid broad home or workspace roots, and monitor the dashboard and generated results during initial use. <br>


## Reference(s): <br>
- [Server-resolved GitHub repository](https://github.com/handsomestWei/loop-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and task-plan tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write or update repository planning files and start persistent loop or dashboard processes when invoked.] <br>

## Skill Version(s): <br>
0.1.0 (source: target metadata and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
