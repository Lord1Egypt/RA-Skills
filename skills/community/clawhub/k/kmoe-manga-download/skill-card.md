## Description: <br>
Download manga from Kmoe (kxx.moe / mox.moe) with concurrent downloads, credential management, and automation callbacks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[InphinitiZ](https://clawhub.ai/user/InphinitiZ) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to operate the kmdr command-line tool for downloading Kmoe manga volumes, managing Kmoe credentials and credential pools, configuring mirrors or proxies, and setting post-download callbacks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports Kmoe account authentication and credential pools. <br>
Mitigation: Prefer interactive password entry instead of passing passwords on the command line, and use only accounts the user is authorized to use. <br>
Risk: Post-download callback commands can execute user-provided shell behavior. <br>
Mitigation: Approve callback commands only after reviewing exactly what they execute. <br>
Risk: The skill depends on the external kmoe-manga-downloader pip package. <br>
Mitigation: Install the package only if the user trusts that external dependency. <br>


## Reference(s): <br>
- [Kmoe Manga Download on ClawHub](https://clawhub.ai/InphinitiZ/kmoe-manga-download) <br>
- [Kmoe mirror source](https://mox.moe) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance centers on the external kmdr CLI, which requires Python >= 3.9 and the kmoe-manga-downloader pip package.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
