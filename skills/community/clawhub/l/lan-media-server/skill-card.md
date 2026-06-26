## Description: <br>
Share images, screenshots, and files from the AI workspace to users on the local network via HTTP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nagellack5C](https://clawhub.ai/user/nagellack5C) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to share generated media or files with users over a local network when the current channel cannot display or transfer them inline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Files placed in the shared folder are accessible on the local network without authentication. <br>
Mitigation: Use a dedicated media folder, place only intended files there, and stop or disable the user service when sharing is no longer needed. <br>
Risk: The setup installs a persistent local-network file server. <br>
Mitigation: Confirm the configured port and MEDIA_ROOT before installation, and keep MEDIA_ROOT pointed at a dedicated sharing directory. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nagellack5C/lan-media-server) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline shell commands and URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local-network HTTP links for files placed in the configured shared directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
