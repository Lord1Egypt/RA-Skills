## Description: <br>
Merlin Security Sentinel helps users secure OpenClaw installations, configure AI agents safely, understand prompt injection and credential risks, and set up governed agentic workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thepoorsatitagain](https://clawhub.ai/user/thepoorsatitagain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and security reviewers use this skill to reason about OpenClaw hardening, prompt-injection exposure, credential handling, malicious skills, and when privileged agent work should run ephemerally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested hardening, gateway, uninstall, or credential-rotation commands may not match a user's OpenClaw setup. <br>
Mitigation: Confirm each command against the local configuration, understand how to undo it, and test changes before applying them to important environments. <br>
Risk: Security claims and architecture guidance could be used for production decisions without independent verification. <br>
Mitigation: Independently verify major security claims and review the guidance with the responsible security or platform team before relying on it for production architecture. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/thepoorsatitagain/merlin-security-sentinel) <br>
- [OpenClaw threat assessment](https://github.com/thepoorsatitagain/OPENCLAW_SECURITY_THREAT_ASSESSMENT3) <br>
- [Hydra Kernel / GEL](https://github.com/thepoorsatitagain/Ai-control-2) <br>
- [Merlin ephemeral sentinel](https://github.com/thepoorsatitagain/Merlin-agenic-security-airgapper) <br>
- [Working OpenClaw wrapper prototype](https://github.com/thepoorsatitagain/working-project-openclaw-wrapper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory content; commands should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
