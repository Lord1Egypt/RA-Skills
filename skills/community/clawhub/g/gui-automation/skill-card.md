## Description: <br>
Control the desktop via the CUA computer server API running on port 8000. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sarinali](https://clawhub.ai/user/sarinali) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to let an agent inspect and operate a local desktop through a temporary localhost CUA server. It supports GUI workflows such as screenshots, clicks, keyboard input, application launch, window control, and form filling when the user intentionally starts the server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent control the user's desktop, including screenshots, mouse actions, keyboard input, file saves, form submissions, and other state-changing actions. <br>
Mitigation: Install only for intentional desktop-control use, run the CUA server temporarily, keep it bound to localhost, stop it when finished, avoid sensitive windows, and confirm actions that save files, submit forms, or change application state. <br>
Risk: Binding the desktop-control server beyond localhost could expose GUI control to other systems on the network. <br>
Mitigation: Keep the server on 127.0.0.1 and avoid network exposure unless the environment has been explicitly secured for that use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sarinali/gui-automation) <br>
- [CUA computer server source](https://github.com/trycua/cua-computer-server) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline bash and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces commands and guidance for interacting with a localhost CUA server; responses may include screenshot data or JSON returned by that server.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
