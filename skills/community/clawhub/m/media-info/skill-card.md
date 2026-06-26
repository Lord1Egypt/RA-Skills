## Description: <br>
Analyze media files with MediaInfo CLI and compare behavior with ffprobe. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KarlZhu-ZXC](https://clawhub.ai/user/KarlZhu-ZXC) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install MediaInfo without root access, inspect media container and codec metadata, troubleshoot files that ffprobe cannot parse, and classify video orientation from width, height, and rotation metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install workflow downloads and builds MediaInfo source code from mediaarea.net, so replacing the source URL or using an unverified archive can introduce supply-chain risk. <br>
Mitigation: Run the installer without root privileges, avoid overriding MEDIAINFO_URL unless the replacement source is trusted, and verify the upstream archive when possible. <br>


## Reference(s): <br>
- [ClawHub media-info release](https://clawhub.ai/KarlZhu-ZXC/media-info) <br>
- [MediaInfo CLI source archive used by the installer](https://mediaarea.net/download/binary/mediainfo/0.7.94/MediaInfo_CLI_0.7.94_GNU_FromSource.tar.bz2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional MediaInfo plain-text or JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the inspected media file and the locally built MediaInfo CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
