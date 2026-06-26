## Description: <br>
Control ONVIF Profile S/T IP cameras for PTZ, presets, discovery, and RTSP snapshot or recording with multi-camera support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ltpop](https://clawhub.ai/user/ltpop) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to let an agent discover, configure, and control owned or administered ONVIF IP cameras, including PTZ movement, presets, RTSP snapshots, and short recordings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Camera credentials may be exposed through stream URLs or plaintext configuration. <br>
Mitigation: Avoid sharing stream-url output, prefer environment variables or a protected config file, and restrict config file permissions. <br>
Risk: The skill can capture video or move cameras that the agent can access. <br>
Mitigation: Install and run it only for cameras the user owns or administers, and review recording, snapshot, PTZ, preset, discovery, and add operations before execution. <br>


## Reference(s): <br>
- [Ipcam ClawHub release page](https://clawhub.ai/ltpop/ipcam) <br>
- [README](README.md) <br>
- [Skill documentation](SKILL.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create camera configuration, snapshots, and short recording files when the generated commands are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, frontmatter, and CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
