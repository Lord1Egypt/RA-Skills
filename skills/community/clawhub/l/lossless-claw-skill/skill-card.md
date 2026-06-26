## Description: <br>
Skill completo para lossless-claw (LCM). Incluye instrucciones para instalar el plugin automaticamente. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yejay7](https://clawhub.ai/user/yejay7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install or verify the third-party lossless-claw plugin, restart the OpenClaw gateway, and run LCM commands for searching and expanding retained conversation history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to install a third-party OpenClaw plugin and restart the OpenClaw gateway. <br>
Mitigation: Require explicit user approval before installation or restart, and install only after reviewing and trusting the external plugin source. <br>
Risk: The plugin retains and searches local conversation history, which can include sensitive prior content. <br>
Mitigation: Confirm retention and deletion behavior before sensitive use, avoid searching for secrets unless necessary, and disable or remove retained history when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/yejay7/lossless-claw-skill) <br>
- [Publisher profile](https://clawhub.ai/user/yejay7) <br>
- [lossless-claw GitHub project](https://github.com/Martian-Engineering/lossless-claw) <br>
- [Lossless Context documentation](https://losslesscontext.ai) <br>
- [LCM paper](https://papers.voltropy.com/LCM) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent through plugin installation, gateway restart, LCM command usage, and troubleshooting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
