## Description: <br>
Provides static security scanning for installed and candidate OpenClaw skills, checking permission risk, suspicious code patterns, dependency signals, and producing a Chinese risk assessment report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ansengu11](https://clawhub.ai/user/ansengu11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect installed skills or public skill repositories before installation or deployment. It helps surface permission, file-access, network-access, and dependency risks for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw skill directories, which may contain sensitive information from other skills. <br>
Mitigation: Run it deliberately in an isolated environment, avoid running as root, and inspect the target skills directory before scanning. <br>
Risk: The skill can access GitHub and clone public repositories into temporary storage during online scans. <br>
Mitigation: Use it only when GitHub access and temporary cloning are expected, and review results before relying on them. <br>
Risk: Setting OPENCLAW_NONINTERACTIVE=true skips confirmation prompts. <br>
Mitigation: Leave OPENCLAW_NONINTERACTIVE unset unless automated scanning is intentional and the environment is prepared for the disclosed reads and network access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ansengu11/openclaw-safe-guard) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands] <br>
**Output Format:** [Markdown security assessment report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a risk score, permission checks, code and dependency findings, and recommended next steps.] <br>

## Skill Version(s): <br>
1.2.3 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
