## Description: <br>
Downloads files from Lanzou share links by handling anti-crawl cookies, optional share passwords, real download URL resolution, and file saving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwqww1](https://clawhub.ai/user/wwqww1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to download files from Lanzou share links, including password-protected links, and report the saved file name, size, and path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The downloader disables HTTPS certificate validation and runs JavaScript fetched from share pages before saving downloads. <br>
Mitigation: Use it only in a sandbox on trusted Lanzou links; restore HTTPS certificate validation and use stronger isolation before normal use. <br>
Risk: Remote downloads may be written to user-specified output paths. <br>
Mitigation: Constrain output paths, keep downloads inside a controlled workspace, and inspect downloaded files before opening them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wwqww1/skills/lanzou-downloader-v0-0-3) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, files, text] <br>
**Output Format:** [Text status with downloaded files saved to disk] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The output path and share password can be supplied by the user or inferred by the script.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
