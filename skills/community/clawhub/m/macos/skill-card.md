## Description: <br>
macOS system administration, command-line differences from Linux, and automation best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill for macOS administration guidance, especially when adapting Linux-oriented command-line workflows and automation to macOS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes examples for commands that can read secrets, access clipboard or screenshots, use sudo, change network or power settings, alter privacy permissions, create launchd jobs, or modify quarantine attributes. <br>
Mitigation: Require explicit confirmation before applying those commands and review their target paths, permissions, and side effects before execution. <br>
Risk: macOS administration guidance may be copied into local automation where incorrect use can affect user privacy, security settings, or system behavior. <br>
Mitigation: Treat the output as reference material, test changes in a controlled environment, and prefer least-privilege execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/macos) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reference guidance only; no executable code is included in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
