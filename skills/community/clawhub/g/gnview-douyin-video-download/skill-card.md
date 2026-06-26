## Description: <br>
Download Douyin videos without watermark by using curl with a Referer header to bypass anti-leech protection and save files to configured paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gnview](https://clawhub.ai/user/gnview) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to generate curl-based guidance for downloading Douyin video files to a chosen local path. It is intended for content they are authorized to download. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to bypass Douyin anti-leech restrictions and download no-watermark videos, which may be inappropriate for content the user is not authorized to download. <br>
Mitigation: Use it only for content you have rights to download, and review the generated curl command before running it. <br>
Risk: Generated download commands can overwrite local files when the output path or filename collides with an existing file. <br>
Mitigation: Save downloads to a dedicated folder with unique filenames and confirm the destination path before execution. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands depend on a current Douyin playback URL and a writable local download directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
