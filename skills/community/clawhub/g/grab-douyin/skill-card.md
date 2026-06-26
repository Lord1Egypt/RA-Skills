## Description: <br>
Downloads Douyin videos through the TikHub API from short links, full URLs, query parameters, or bare video IDs, with optional saving to disk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mfang0126](https://clawhub.ai/user/mfang0126) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to resolve Douyin video links or IDs and retrieve either a direct video URL or a downloaded MP4 file. It is intended for Douyin videos only, not live streams, image carousels, or other video platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to run when a Douyin link or numeric video ID is merely detected. <br>
Mitigation: Require explicit user confirmation before contacting TikHub or downloading files. <br>
Risk: Douyin links or video IDs and a local TikHub API token are used with a third-party API. <br>
Mitigation: Install only when this data sharing is acceptable, store the token in ~/.openclaw/config.json, and avoid sharing sensitive or private video identifiers. <br>
Risk: The downloader is limited to Douyin videos and may fail for live streams, image carousels, private, deleted, or unsupported videos. <br>
Mitigation: Use it only for supported Douyin video links or 16-19 digit IDs and review failures before retrying with other tools. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mfang0126/grab-douyin) <br>
- [TikHub API token registration](https://user.tikhub.io/register) <br>
- [TikHub Douyin fetch-one-video endpoint](https://api.tikhub.io/api/v1/douyin/web/fetch_one_video) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May print a Douyin modal_id, direct video URL, or saved MP4 path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
