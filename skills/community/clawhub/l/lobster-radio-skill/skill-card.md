## Description: <br>
Personalized news-radio generation service for creating topic-based audio briefings, scheduled pushes, TTS voice configuration, and playback of generated radio history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jayden-X-L](https://clawhub.ai/user/Jayden-X-L) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn user-selected topics or tags into local TTS news-radio audio, configure voice settings, schedule recurring briefings, and retrieve prior generated radio items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local/offline privacy claims conflict with model downloads, platform LLM or web-search use, and scheduled automation. <br>
Mitigation: Review network behavior before use, avoid sensitive radio topics, and run the skill in an isolated environment until privacy claims are reconciled. <br>
Risk: The skill can create persistent scheduled tasks and write generated audio or configuration files locally. <br>
Mitigation: Inspect scheduled tasks after creation and restrict output locations to expected OpenClaw or user-selected folders. <br>
Risk: Model and dependency downloads may use unpinned or externally hosted artifacts. <br>
Mitigation: Prefer pinned, verified model and dependency versions and review downloaded artifacts before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Jayden-X-L/lobster-radio-skill) <br>
- [Qwen3-TTS model on Hugging Face](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice) <br>
- [Qwen3-TTS model on ModelScope](https://modelscope.cn/models/qwen/Qwen3-TTS-12Hz-0.6B-Base) <br>
- [Qwen3-TTS blog](https://qwen.ai/blog?id=qwen3tts-0115) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [LobsterAI project](https://github.com/netease-youdao/LobsterAI) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown responses with audio file links, text summaries, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local audio files and configuration state, and may use scheduled tasks for recurring generation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
