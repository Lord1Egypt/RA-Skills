## Description: <br>
Generate music using MiniMax music-2.6 or music-cover API and send it as a Feishu MP3 audio attachment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raydoomed](https://clawhub.ai/user/raydoomed) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Feishu users use this skill to generate original or cover-mode songs from prompts, lyrics, and optional reference audio, then send the resulting MP3 to a Feishu recipient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, lyrics, cover audio, recipient IDs, and generated music may be sensitive. <br>
Mitigation: Use only non-sensitive inputs and recipient IDs unless the deployment has appropriate consent, retention, and data-handling controls. <br>
Risk: MiniMax and Feishu credentials are required and can be exposed if configuration files are mishandled. <br>
Mitigation: Protect music_config.json and openclaw.json as secrets, restrict file permissions, and avoid committing or sharing credential-bearing files. <br>
Risk: The title argument is used as an output filename and may write outside the intended songs folder if unsafe path components are provided. <br>
Mitigation: Avoid absolute paths or parent-directory segments in --title and prefer a release that sanitizes output filenames before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/raydoomed/minimax-feishu-music) <br>
- [MiniMax music generation API endpoint](https://api.minimaxi.com/v1/music_generation) <br>
- [Feishu tenant token API endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown with bash commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can call external MiniMax and Feishu APIs and can create MP3 files in the OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.4.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
