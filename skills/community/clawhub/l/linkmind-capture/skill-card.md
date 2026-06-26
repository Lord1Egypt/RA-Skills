## Description: <br>
Capture social media links from Weibo, Xiaohongshu, WeChat, and Xiaoyuzhou; extract text, images, metadata, and optional transcripts; then generate a Markdown note with an AI deep summary saved to the user's Obsidian vault. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tt-bltn](https://clawhub.ai/user/tt-bltn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to capture supported social media and podcast links into Obsidian as structured Markdown notes with source content, media references, metadata, and Chinese deep summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes notes and downloaded media into the configured Obsidian vault. <br>
Mitigation: Use a dedicated or backed-up vault path and review generated notes and attachments before relying on them. <br>
Risk: The skill may use platform cookies and a local Chrome debugging session to access supported sites. <br>
Mitigation: Prefer a dedicated or low-privilege social account, avoid broad session cookies, and review the .env file before use. <br>
Risk: Media may be sent to configured ASR services for transcription. <br>
Mitigation: Enable ASR only with trusted providers and avoid processing sensitive audio or video unless the external processing is acceptable. <br>
Risk: The Xiaohongshu workflow includes anti-bot evasion behavior that may conflict with platform rules. <br>
Mitigation: Confirm platform terms and disable or avoid that workflow where compliance is uncertain. <br>


## Reference(s): <br>
- [LinkMind GitHub Repository](https://github.com/tt-bltn/LinkMind) <br>
- [ClawHub Skill Page](https://clawhub.ai/tt-bltn/linkmind-capture) <br>
- [Deep Summary Guidelines](references/deep-summary-guide.md) <br>
- [OpenAI API Keys](https://platform.openai.com/api-keys) <br>
- [iFlytek](https://www.xfyun.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown notes with YAML frontmatter, inline media references, metadata, transcript excerpts, and user-facing status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes notes and downloaded assets under the configured Obsidian vault; handler scripts emit JSON used by the agent workflow.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
