## Description: <br>
A music download manager that searches YouTube or Bilibili, downloads audio, converts it to MP3, and stores it in a local music library by category. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2771096196](https://clawhub.ai/user/2771096196) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users can use this skill to search for music or pass a YouTube/Bilibili URL, then download the audio as an MP3 into a chosen local category folder. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The downloader can access local browser cookies when browser-based authentication is enabled. <br>
Mitigation: Set BROWSER = None unless authenticated downloads are required, and avoid using a main browser profile for downloads. <br>
Risk: Unsafe category input can place downloaded files outside the intended music library. <br>
Mitigation: Use only simple category names and reject absolute paths or values containing ../ before running the script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/2771096196/music-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline bash commands and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces MP3 files in a configured local music directory when the download script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
