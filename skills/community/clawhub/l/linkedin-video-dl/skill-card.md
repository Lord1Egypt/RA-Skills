## Description: <br>
Downloads videos from public LinkedIn posts as MP4 files without authentication or external dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpnarchi](https://clawhub.ai/user/jpnarchi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to build or run a zero-dependency Go CLI that downloads MP4 video files from public LinkedIn post URLs. It is intended for public posts the user has rights to download. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The downloader fetches public LinkedIn post pages and video CDN URLs, which may be rate-limited or blocked if used excessively. <br>
Mitigation: Run it only for public posts you have rights to download and avoid excessive automated use. <br>
Risk: The CLI writes MP4 and .tmp files in the current directory. <br>
Mitigation: Run it from a directory where creating those files is acceptable and review generated filenames before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpnarchi/linkedin-video-dl) <br>
- [Publisher profile](https://clawhub.ai/user/jpnarchi) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and Go source code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a Go CLI workflow that writes MP4 files and temporary .tmp files to the current directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
