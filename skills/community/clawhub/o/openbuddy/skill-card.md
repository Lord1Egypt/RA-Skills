## Description: <br>
OpenBuddy 电子宠物系统 - 在你的终端中孵化、养成和互动虚拟宠物伙伴 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wltgithub](https://clawhub.ai/user/wltgithub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and terminal users use OpenBuddy to hatch, view, pet, mute, and talk with a local ASCII virtual pet during AI coding sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local Node script that creates or updates a small state file under ~/.openbuddy by default. <br>
Mitigation: Review commands before execution and set OPENBUDDY_DIR to choose a different storage path. <br>
Risk: The default pet generation seed uses local hostname and username environment values. <br>
Mitigation: Set OPENBUDDY_USER_ID to avoid using the default machine/user-derived seed. <br>


## Reference(s): <br>
- [OpenBuddy ClawHub skill page](https://clawhub.ai/wltgithub/openbuddy) <br>
- [wltgithub ClawHub publisher profile](https://clawhub.ai/user/wltgithub) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local Node commands may create or update ~/.openbuddy/buddy-soul.json unless OPENBUDDY_DIR is set.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
