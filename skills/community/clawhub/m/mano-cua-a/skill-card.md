## Description: <br>
Computer use for GUI automation tasks via VLA models when the user describes a natural-language task that requires visual screen interaction and no API or CLI exists for the target app. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoluohei](https://clawhub.ai/user/xiaoluohei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to automate foreground desktop apps or webpages from natural-language task descriptions when API or CLI automation is unavailable. It supports local on-device mode for privacy-sensitive tasks and cloud mode for more complex visual reasoning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool can see the primary display and control mouse and keyboard input during a user-started session. <br>
Mitigation: Install only when that level of desktop automation is acceptable, keep unrelated private windows out of view, and supervise active sessions. <br>
Risk: Cloud mode may send primary-display screenshots transiently for inference. <br>
Mitigation: Use local mode for privacy-sensitive tasks and avoid displaying confidential information when cloud mode is active. <br>
Risk: Purchases, credential entry, deletions, financial actions, or account changes can have irreversible effects. <br>
Mitigation: Require user confirmation for sensitive actions and personally review the screen before approving each step. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaoluohei/mano-cua-a) <br>
- [Publisher profile](https://clawhub.ai/user/xiaoluohei) <br>
- [Mano skill repository](https://github.com/Mininglamp-AI/mano-skill) <br>
- [Mano skill releases](https://github.com/Mininglamp-AI/mano-skill/releases) <br>
- [Mano-P model](https://huggingface.co/Mininglamp-2718/Mano-P) <br>
- [Network model module](https://github.com/Mininglamp-AI/mano-skill/blob/main/visual/model/task_model.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command options for installing, launching, stopping, or configuring mano-cua; the skill itself does not produce persistent files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
