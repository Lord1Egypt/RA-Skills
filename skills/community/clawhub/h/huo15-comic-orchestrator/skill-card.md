## Description: <br>
Orchestrates a multi-step AI comic-drama workflow that turns a theme into script, characters, storyboards, generated video, dubbing, lip sync, background music, subtitles, and a final assembled short video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and developers use this skill to coordinate a Chinese-style AI comic-drama production pipeline with budget checks, confirmation gates, checkpointed execution, and resumable output generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can launch paid external media-generation services through sibling skills. <br>
Mitigation: Keep confirmation enabled, set a cost cap before execution, and avoid --auto-confirm unless the budget and provider account limits are already approved. <br>
Risk: The release requires sensitive provider credentials such as ARK_API_KEY. <br>
Mitigation: Store provider credentials outside prompts and skill files, limit provider-account spend, and rotate keys if exposed. <br>
Risk: Prompts or media may be sent to configured external AI services. <br>
Mitigation: Do not submit private prompts or media unless the user accepts the configured providers' handling of that data. <br>
Risk: The security summary notes that the orchestrator depends on the broader huo15 comic skill family. <br>
Mitigation: Install and review the complete skill family, not only this orchestrator, before running the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/huo15-comic-orchestrator) <br>
- [Volcengine Seedance documentation](https://www.volcengine.com/docs/82379/1520757) <br>
- [Volcengine TTS documentation](https://www.volcengine.com/docs/6561/97465) <br>
- [Kling API](https://api.klingai.com/v1) <br>
- [Suno API provider](https://api.sunoapi.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance, shell commands, JSON project artifacts, cost reports, and final media file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided project inputs and may generate local output files such as script.json, checkpoint data, audio/video assets, and final.mp4.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
