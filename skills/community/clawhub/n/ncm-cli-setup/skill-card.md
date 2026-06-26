## Description: <br>
Installs and configures ncm-cli for NetEase Cloud Music CLI use, including API key setup, mpv player installation, player selection, login, and basic troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JunfengL](https://clawhub.ai/user/JunfengL) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users use this skill to install ncm-cli, configure required API credentials, set up mpv or a local NetEase Cloud Music player, log in, and troubleshoot common setup issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing ncm-cli and mpv may run npm, package-manager, or sudo commands that modify the local system. <br>
Mitigation: Review each installation command and package-manager prompt before approving it, and install only when ncm-cli or local playback is intended. <br>
Risk: appId, privateKey, and login state are sensitive setup inputs. <br>
Mitigation: Avoid entering or displaying credentials in shared, logged, or recorded terminals. <br>


## Reference(s): <br>
- [NetEase Cloud Music Open Platform API key application](https://developer.music.163.com/st/developer/apply/account?type=INDIVIDUAL) <br>
- [mpv installation](https://mpv.io/installation/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes platform-specific package-manager guidance and credential-handling cautions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
