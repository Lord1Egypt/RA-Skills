## Description: <br>
Configure Google Drive mount on Linux via rclone + gog OAuth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonglinmu](https://clawhub.ai/user/tonglinmu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Linux users use this skill to configure rclone with gog OAuth credentials, mount Google Drive as a local filesystem, and enable a systemd auto-mount on boot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup handles long-lived Google Drive refresh tokens and client secrets. <br>
Mitigation: Protect gog and rclone credential files with owner-only permissions and run the setup only on a trusted single-user Linux machine. <br>
Risk: The setup writes rclone configuration and may replace an existing rclone.conf. <br>
Mitigation: Back up any existing rclone configuration before running the setup. <br>
Risk: The setup creates a boot-persistent systemd mount service. <br>
Mitigation: Confirm that an automatic Google Drive mount is intended and know how to disable it with systemctl disable --now rclone-gdrive. <br>
Risk: The rclone mount uses --allow-other, which can expose mounted files to other local users. <br>
Mitigation: Avoid --allow-other unless it is required for the environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tonglinmu/google-drive-setup) <br>
- [Google OAuth token endpoint](https://oauth2.googleapis.com/token) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with inline bash and ini configuration blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that write rclone configuration and install a systemd mount service.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
