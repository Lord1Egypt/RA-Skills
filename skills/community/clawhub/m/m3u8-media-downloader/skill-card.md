## Description: <br>
Use @lzwme/m3u8-dl to parse video information and download m3u8/HLS, mp4, and mp3 media from URLs provided by the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renxia](https://clawhub.ai/user/renxia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other users use this skill when they need an agent to produce safe command guidance for parsing media metadata, downloading m3u8/HLS, mp4, or mp3 media, or running the optional local WebUI for download tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill helps run a media downloader and ffmpeg against user-provided URLs, which can fetch remote content and write files locally. <br>
Mitigation: Install only the pinned downloader package and a trusted ffmpeg build, run downloads in a dedicated directory, and review destination paths before execution. <br>
Risk: Custom request headers or cookies may expose private authorization data when used for downloads. <br>
Mitigation: Avoid passing private cookies or authorization headers unless they are necessary, and remove sensitive values from prompts, logs, and saved command history. <br>
Risk: The optional local WebUI can expose download controls if it is left unprotected. <br>
Mitigation: Protect the WebUI with a strong secret or token and use it only in a trusted local environment. <br>
Risk: Media downloads can violate source site terms or applicable law. <br>
Mitigation: Confirm that each download is authorized and complies with the source site's terms and local legal requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/renxia/m3u8-media-downloader) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command examples for m3u8dl, ffmpeg path settings, output filenames, save directories, request headers, and local WebUI options.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
