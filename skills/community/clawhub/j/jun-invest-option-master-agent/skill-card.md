## Description: <br>
OpenClaw Agent App Installer: install/upgrade and register the jun-invest-option-master-agent isolated agent workspace, including automatic backup and versioning to ClawHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gm4leejun-stack](https://clawhub.ai/user/gm4leejun-stack) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users who manage this specific isolated investment-agent workspace use the skill to install or upgrade the agent, register it, keep runtime assets synchronized, and generate human-reviewed investment approval packets. The included investment workflow is designed to produce proposals and validation artifacts, not to place trades automatically. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic commits, post-commit synchronization, and launchd publishing can publish local workspace changes or personal configuration unexpectedly. <br>
Mitigation: Install only in the intended workspace, review or disable the git hook and launchd job before use, and keep tokens, account details, and personal profile data outside the packaged artifact. <br>
Risk: The installer registers an OpenClaw agent and best-effort installs external skills at their latest available versions. <br>
Mitigation: Review the installer scripts and external skill list before installation, and run the doctor or validation scripts after installation to confirm the workspace matches expectations. <br>
Risk: Investment outputs may be incorrect, incomplete, or unsuitable for a real portfolio if used without review. <br>
Mitigation: Treat generated approval packets as proposals only; require human approval, enforce the policy and validator checks, and do not use the skill to place trades automatically. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gm4leejun-stack/jun-invest-option-master-agent) <br>
- [OpenClaw documentation](https://docs.openclaw.ai/) <br>
- [Futu OpenAPI documentation](https://openapi.futunn.com/futu-api-doc/intro/intro.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, generated approval packets, and JSON validation reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Installs and registers an OpenClaw isolated workspace; investment outputs are intended for human approval and do not execute trades automatically.] <br>

## Skill Version(s): <br>
0.2.202603041248 (source: server release metadata; artifact _meta.json reports 0.2.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
