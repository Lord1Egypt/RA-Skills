## Description: <br>
Harden OpenClaw (workspace + ~/.openclaw): run openclaw security audit, catch prompt-injection/exfil risks, scan for secrets, and apply safe fixes (chmod/exec-bit cleanup). Includes optional config.patch planning to reduce attack surface. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[virtaava](https://clawhub.ai/user/virtaava) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to check and harden an OpenClaw workspace and user configuration. It supports read-only audits by default, explicit safe fixes, and optional configuration patch planning for reduced attack surface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects repository files and ~/.openclaw state and can run local OpenClaw, git, Python, bash, and scanner commands. <br>
Mitigation: Install only if that local access is acceptable, and run it in a clean working tree or test OpenClaw profile first. <br>
Risk: Fix and apply-config modes can change filesystem permissions or OpenClaw gateway configuration. <br>
Mitigation: Use the default read-only check mode first, review proposed fixes or config.patch output, and run mutation modes only after explicit approval. <br>
Risk: Security or configuration findings could include sensitive local data if command output is not handled carefully. <br>
Mitigation: Rely on the skill's redaction behavior and avoid sharing raw outputs until they have been reviewed for secrets. <br>


## Reference(s): <br>
- [OpenClaw Hardener release page](https://clawhub.ai/virtaava/openclaw-hardener) <br>
- [virtaava publisher profile](https://clawhub.ai/user/virtaava) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON output from the hardening script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script can emit human-readable findings or JSON findings, and config planning prints a JSON patch plus review notes.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence and openclaw-skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
