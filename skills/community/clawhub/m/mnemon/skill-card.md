## Description: <br>
Persistent memory CLI for LLM agents that stores facts, recalls past knowledge, links related memories, and manages the memory lifecycle. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Grivn](https://clawhub.ai/user/Grivn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and LLM-agent users use Mnemon Memory to install and configure persistent cross-session memory for OpenClaw, then remember, recall, link, search, forget, and manage stored memories through the mnemon CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent cross-session memory and OpenClaw hooks can affect future agent behavior. <br>
Mitigation: Review the generated OpenClaw hook and plugin settings after setup, enable only desired hooks, and use eject, forget, gc, store removal, or related lifecycle controls when stored memory or installed hooks are no longer wanted. <br>
Risk: Stored memories may capture sensitive information if users save secrets or tokens. <br>
Mitigation: Avoid saving secrets, passwords, or tokens, and remove any unwanted stored memories with the available forget, gc, and store-management commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Grivn/mnemon) <br>
- [Publisher profile](https://clawhub.ai/user/Grivn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides installation, setup, recall, remember, link, lifecycle, and storage-management workflows for the mnemon CLI.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
