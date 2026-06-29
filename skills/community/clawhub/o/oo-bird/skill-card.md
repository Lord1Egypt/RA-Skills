## Description: <br>
Bird (bird.com). Use this skill for Bird requests involving reading, creating, updating, deleting data, and sending messages through the OOMOL `oo` CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Bird contacts, channels, messages, and message interactions through an OOMOL-connected Bird account. It supports read workflows as well as guarded write and destructive actions such as contact updates, message sends, and contact deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The trigger wording is broad and may route many Bird-related requests toward live Bird data operations. <br>
Mitigation: Install and invoke the skill only when the user intends the agent to work with Bird data, and confirm the intended workspace, action, and target before running state-changing commands. <br>
Risk: Write and destructive actions can create, update, send, or delete customer and messaging data. <br>
Mitigation: Review the exact payload and expected effect before writes, and require explicit approval for destructive actions such as deleting contacts. <br>


## Reference(s): <br>
- [Bird homepage](https://bird.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before building action payloads; connector responses are JSON with data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
