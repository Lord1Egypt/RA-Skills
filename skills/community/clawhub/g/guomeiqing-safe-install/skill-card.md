## Description: <br>
Safely reviews and installs third-party OpenClaw Skills by downloading to a temporary directory, running a seven-point security audit, generating a human-readable report, and installing only when safe. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shanggqm](https://clawhub.ai/user/shanggqm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to review third-party skill sources before installation, produce a security report, and install only skills that pass the defined checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch third-party repositories or npm packages and persist reviewed content into the user's OpenClaw skills folder. <br>
Mitigation: Use trusted sources, inspect the generated report, and proceed only when the review result and source are acceptable. <br>
Risk: Source strings with shell-like punctuation could affect local shell commands used during review or installation. <br>
Mitigation: Avoid shell-like punctuation in source inputs and review generated commands before execution. <br>
Risk: Manual bypass commands for dangerous skills can override the review outcome. <br>
Mitigation: Use manual installation only after independently reviewing the package in isolation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shanggqm/guomeiqing-safe-install) <br>
- [README.en.md](artifact/README.en.md) <br>
- [SKILL.en.md](artifact/SKILL.en.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command blocks and a structured security review report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only skill; operations are proposed through the agent's tool use rather than bundled executable scripts.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
