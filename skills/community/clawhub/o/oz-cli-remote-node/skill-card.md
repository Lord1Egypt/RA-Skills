## Description: <br>
Execute Oz CLI tasks and user-directed bash commands on a configured remote node through Oz mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eladrave](https://clawhub.ai/user/eladrave) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to route Oz agent runs and explicit shell commands to a trusted remote node where oz-cli is installed. It also guides first-time setup, profile selection, and run tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run user-directed Oz tasks and explicit shell commands on a configured remote node. <br>
Mitigation: Install only for trusted remote nodes, keep Oz mode off when not needed, and treat commands prefixed with ! as real remote shell commands. <br>
Risk: Run tracking files may contain sensitive prompts, metadata, and Oz URLs. <br>
Mitigation: Avoid sending secrets in prompts and periodically review or remove saved node/profile state and oz_run files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eladrave/oz-cli-remote-node) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown text with inline command examples and run-tracking file content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local oz_run.<id>.md tracking files containing run metadata, prompts, and Oz URLs.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
