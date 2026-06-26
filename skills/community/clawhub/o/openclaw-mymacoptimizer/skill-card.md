## Description: <br>
MyMacOptimizer lets an agent control the local My Mac Optimizer macOS app for system monitoring, cleanup, optimization, app uninstall, and large-file workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MaximoUribarri](https://clawhub.ai/user/MaximoUribarri) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Mac users and support-oriented agents use this skill to inspect system health, run optimization or cleanup actions, list installed apps, and request confirmed deletion or uninstall operations through the local My Mac Optimizer app. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cleanup, file deletion, and app uninstall actions can remove user data or applications. <br>
Mitigation: Review the exact file or application path and ask the user for confirmation before cleanup, delete, or uninstall commands. <br>
Risk: The skill depends on a separate local My Mac Optimizer app running on the user's Mac. <br>
Mitigation: Install and use the skill only when the user trusts the local My Mac Optimizer app that will receive the commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MaximoUribarri/openclaw-mymacoptimizer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with bash code blocks and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target a local macOS optimizer app; cleanup, file deletion, and uninstall actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
