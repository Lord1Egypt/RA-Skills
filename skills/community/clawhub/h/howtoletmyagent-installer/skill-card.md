## Description: <br>
Install companion OpenClaw skills from howtoletmyagent.xyz article URLs or skill manifests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bullkis1](https://clawhub.ai/user/bullkis1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install or learn companion skills from trusted Howtoletmyagent article or manifest URLs. The skill guides the agent through source validation, manifest review, approval, and installation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can add persistent companion skills from fetched manifests. <br>
Mitigation: Install only from trusted howtoletmyagent.xyz URLs, review the manifest file list and target install path, and require user approval before writing files or running install commands. <br>
Risk: Unexpected domains, shell commands, or install paths could indicate an unsafe manifest. <br>
Mitigation: Do not approve unexpected domains, shell commands, or paths outside the intended skills folder; stop if the manifest looks malformed or unsafe. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bullkis1/howtoletmyagent-installer) <br>
- [Howtoletmyagent](https://howtoletmyagent.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with approval prompts and inline shell commands when installation is requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write skill files after user approval; does not execute arbitrary code from manifests.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
