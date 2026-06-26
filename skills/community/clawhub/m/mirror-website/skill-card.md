## Description: <br>
Mirrors static or server-rendered websites to a local folder for offline browsing, with steps for downloading assets, cleaning filenames and links, validating the mirror, and starting a local preview server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenbing3049](https://clawhub.ai/user/wenbing3049) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to create local, offline copies of websites they own or are authorized to copy, then inspect and preview the mirrored result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can mirror websites and includes commands that bypass certificate checks or robots.txt policy. <br>
Mitigation: Use only sites you own or are authorized to copy, review each command before execution, and remove bypass flags unless they are explicitly needed. <br>
Risk: The workflow writes downloaded content and helper scripts into a user-selected local directory. <br>
Mitigation: Choose a new empty destination folder and verify the resolved path before running file-creation or cleanup steps. <br>
Risk: The workflow may use a local proxy and start a background preview server. <br>
Mitigation: Confirm proxy use before routing traffic through it, bind preview serving to localhost, record the PID, and stop the server when finished. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wenbing3049/mirror-website) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and generated shell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a local website mirror, helper shell scripts, validation output, and a localhost preview server.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
