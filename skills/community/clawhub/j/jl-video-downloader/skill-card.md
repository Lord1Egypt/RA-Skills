## Description: <br>
JL Video Downloader helps agents download videos and extract transcripts from Douyin, Kuaishou, Xiaohongshu, Bilibili, YouTube, and other yt-dlp-supported platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pyzxs](https://clawhub.ai/user/pyzxs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to inspect video metadata, download media, batch-process URL lists, and extract spoken content into text for downstream workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can modify shell startup files and create persistent environment-loading behavior. <br>
Mitigation: Review setup.sh before running it, back up shell startup files, and prefer manual configuration when persistence is not required. <br>
Risk: The wrapper builds a command string and executes it with eval, increasing exposure to unsafe URL or argument handling. <br>
Mitigation: Use only trusted URLs and arguments, inspect the resolved command before execution, and replace eval with array-based command invocation before broad deployment. <br>
Risk: The setup flow can install or upgrade external package code and suggests curl | sh for uv installation. <br>
Mitigation: Install dependencies manually from trusted sources, pin versions where possible, and review package provenance before enabling automated installation. <br>
Risk: Example configuration stores API keys and platform cookies in a globally sourced environment file. <br>
Mitigation: Use least-privilege credentials, avoid storing real account cookies in shared shell configuration, and restrict file permissions on local configuration files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pyzxs/jl-video-downloader) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/pyzxs) <br>
- [SiliFlow API](https://siliflow.com) <br>
- [DeepSeek API platform](https://platform.deepseek.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; downloaded media and transcript files are written to a configured output directory.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports single-video and batch URL workflows with optional proxy, API key, segmentation, and output-directory settings.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
