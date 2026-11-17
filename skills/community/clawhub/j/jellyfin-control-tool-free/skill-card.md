## Description: <br>
媒体服务器控制 is a lightweight Jellyfin media server control skill for searching content, resuming playback, discovering controllable devices, and managing playback for personal home entertainment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Personal home media users use this skill to control Jellyfin playback from an agent, including searching for films or episodes, resuming watched content, and issuing playback or TV control commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run commands and issue media or TV control actions. <br>
Mitigation: Review the skill before installation and only enable it for explicit media-control requests. <br>
Risk: Jellyfin and Home Assistant credentials may grant access to personal media systems or home devices. <br>
Mitigation: Use limited-scope tokens where possible and avoid enabling TV power control unless automatic device actions are intended. <br>
Risk: Broad or contradictory activation and limitation instructions may cause the agent to use the skill outside its intended media-control scope. <br>
Mitigation: Tighten routing so the skill activates only for clear Jellyfin playback, search, resume, device discovery, or playback-control requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/jellyfin-control-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce structured success/error responses and command-oriented setup guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
