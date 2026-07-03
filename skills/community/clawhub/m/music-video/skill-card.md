## Description: <br>
Use when the user wants a music video, lyric video, sung promo, or original song paired with performance and B-roll clips. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pruna-ai](https://clawhub.ai/user/pruna-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to plan and run an end-to-end lyric-to-video workflow, including lyrics, song generation, cut alignment, still generation, video clips, and final assembly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lyrics, prompts, uploaded stills, song/audio slices, and related project metadata may be sent to Replicate and Pruna under the user's API keys. <br>
Mitigation: Use only content appropriate for those third-party services, review applicable terms, and avoid submitting secrets or confidential material in plans or prompts. <br>
Risk: Approval or skip flags can advance paid media-generation phases before outputs have been reviewed. <br>
Mitigation: Keep the staged approval gates for lyrics, song, stills, clips, and assembly unless a human has reviewed the current phase. <br>
Risk: Production reproducibility can vary when dependency or external model versions are not pinned. <br>
Mitigation: Pin dependencies and record plan files, seeds, approved assets, and generated outputs for releases that require repeatable results. <br>


## Reference(s): <br>
- [ClawHub music-video skill page](https://clawhub.ai/pruna-ai/skills/music-video) <br>
- [MiniMax Music 2.5 on Replicate](https://replicate.com/minimax/music-2.5) <br>
- [Pruna music-to-video workflow](https://docs.pruna.ai/en/stable/docs_pruna_endpoints/performance_models/workflows/music_to_video.html) <br>
- [Pruna API reference](artifact/references/pruna-api.md) <br>
- [Replicate API reference](artifact/references/replicate-api.md) <br>
- [Staged generation gate](artifact/references/staged-generation-gate.md) <br>
- [Music video quality checklist](artifact/references/music-video-quality-checklist.md) <br>
- [Workflow feedback gates](artifact/references/workflow-feedback-gates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON plan files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local project plans, audio slices, generated media URLs, video clips, and assembled video files through external media APIs and local ffmpeg tooling.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
