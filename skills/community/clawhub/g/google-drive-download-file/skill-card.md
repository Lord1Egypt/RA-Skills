## Description: <br>
Atomic node skill to download a file from Google Drive using the gog CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when they need to download a specific Google Drive file to a local path through the authenticated gog CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes Google Drive content to a local path, so an unsafe or unintended output location could overwrite or expose files. <br>
Mitigation: Use an explicit output path in a safe folder and check whether the file already exists before downloading. <br>
Risk: Downloaded Google Drive content may be untrusted even when the download command succeeds. <br>
Mitigation: Inspect or scan downloaded files before opening, executing, or sharing them. <br>
Risk: The download depends on the local gog CLI and its active Google account authentication. <br>
Mitigation: Install only when the gog CLI is trusted and authenticated to the intended Google account. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/zvirb/google-drive-download-file) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline shell command guidance and a downloaded local file path confirmation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gog binary and an authenticated Google account with access to the requested Drive file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
