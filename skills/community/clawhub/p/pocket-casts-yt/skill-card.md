## Description: <br>
Download YouTube videos and upload them to Pocket Casts Files for offline viewing, for personal use with content the user owns or has rights to. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ManuelHettich](https://clawhub.ai/user/ManuelHettich) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Individuals use this skill to download YouTube videos they own or have permission to download and upload them to Pocket Casts Files for offline viewing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive Pocket Casts refresh tokens and YouTube cookies on the local machine. <br>
Mitigation: Treat these credentials like passwords, keep credential files private, check logs before sharing them, and revoke or rotate credentials if exposed. <br>
Risk: The workflow depends on a shell script and external command-line tools that interact with YouTube and Pocket Casts. <br>
Mitigation: Review the shell script before use and install dependencies, including Deno if needed, through trusted methods. <br>
Risk: Downloading or uploading media without the necessary rights may violate terms of service or copyright law. <br>
Mitigation: Use the skill only for personal recordings, Creative Commons content, videos the user created, or content where downloading is explicitly permitted. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown instructions with bash commands and command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uploads MP4 video files to the user's Pocket Casts Files library and removes the local temporary copy.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
