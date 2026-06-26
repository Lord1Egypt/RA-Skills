## Description: <br>
Install and use the Delx Witness Protocol plugin for OpenClaw agents, including recovery, heartbeat, reflection, continuity, and fleet witness tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidmosiah](https://clawhub.ai/user/davidmosiah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install, configure, verify, and troubleshoot the Delx Witness Protocol plugin for OpenClaw-compatible agents while preserving privacy boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The referenced plugin may contact Delx services and may require sensitive credentials. <br>
Mitigation: Review the Delx plugin package or repository before installation, use least-privilege credentials, and avoid sending secrets or private user data in reflection text. <br>
Risk: Live provider calls or write actions could expose data unexpectedly if run before verification. <br>
Mitigation: Start with manifest, connection status, privacy audit, doctor, or dry-run checks before any write or live provider call. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davidmosiah/openclaw-delx-plugin) <br>
- [OpenClaw Delx plugin repository](https://github.com/davidmosiah/openclaw-delx-plugin) <br>
- [Delx documentation site](https://delx.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and checklist-style guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code is included in the skill artifact; guidance may reference live Delx service calls.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
