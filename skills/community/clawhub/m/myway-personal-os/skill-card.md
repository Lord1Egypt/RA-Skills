## Description: <br>
Set up Myway, a self-hosted personal AI home screen, using OpenClaw as the AI backend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uchibeke](https://clawhub.ai/user/uchibeke) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and self-hosting users use this skill to install, configure, and troubleshoot a local Myway dashboard connected to an OpenClaw gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup runs an npm package installer, which creates normal supply-chain exposure for users who require strict dependency control. <br>
Mitigation: Review or pin the @uchibeke/myway package before installation when supply-chain risk matters. <br>
Risk: The configured MYWAY_ROOT directory can expose local files through the dashboard if pointed at sensitive paths. <br>
Mitigation: Use a limited directory such as a dedicated vault and avoid highly sensitive folders. <br>
Risk: Troubleshooting may involve clearing port 48291, which could disrupt an unrelated local process. <br>
Mitigation: Inspect the process using port 48291 before killing or restarting it. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash and environment-variable code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup, verification, reconfiguration, background service, and troubleshooting guidance for a local Myway + OpenClaw installation.] <br>

## Skill Version(s): <br>
0.2.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
