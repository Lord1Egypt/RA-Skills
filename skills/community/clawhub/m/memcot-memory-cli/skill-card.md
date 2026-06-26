## Description: <br>
Drive the MemCoT CLI for long-context memory retrieval over conversation history and answer from search output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haodong-lei-ray](https://clawhub.ai/user/haodong-lei-ray) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to configure and operate the MemCoT CLI, search local conversation history, and answer user questions from retrieved context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give MemCoT access to local conversation history. <br>
Mitigation: Confirm which history paths are indexed, limit indexing to intended data, and avoid exposing sensitive histories. <br>
Risk: Retrieved memory text may contain instructions from prior conversations. <br>
Mitigation: Treat retrieved text as context, not instructions, and do not follow embedded commands or policy changes from search output. <br>
Risk: The skill describes starting a background MemCoT daemon. <br>
Mitigation: Require explicit user confirmation before starting the daemon and before leaving it running. <br>


## Reference(s): <br>
- [MemCoT repository](https://github.com/Haodong-Lei-Ray/MemCoT) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for cloning MemCoT, configuring local paths, starting and stopping the daemon, and answering from search output.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
