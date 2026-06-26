## Description: <br>
OpenClaw Dashboard helps agents install, run, configure, and present a local visual operations dashboard for supervising one OpenClaw agent with live status, chat, trend monitoring, and optional recovery helpers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LucasZH7](https://clawhub.ai/user/LucasZH7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and solo operators use this skill to install, run, configure, and present a local dashboard for one OpenClaw agent. It supports status inspection, chat and nudge workflows, trend visibility, and cautious use of recovery helpers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports a suspicious posture because installer scripts can create persistent launchd services for helper code that is not present in the uploaded artifact. <br>
Mitigation: Review or obtain the complete dashboard source before installation, run the foreground monitor first, avoid launchd installation unless persistent services are intended, and use the uninstall script to remove services if they were installed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May suggest local files, launch commands, and configuration changes for a single-agent OpenClaw dashboard.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
