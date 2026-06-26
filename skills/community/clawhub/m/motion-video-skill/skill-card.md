## Description: <br>
Generates structured explainer animation videos from text, scripts, or Markdown by building editable movie.json projects, rendering web previews, and exporting MP4 only after explicit confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mr-q526](https://clawhub.ai/user/mr-q526) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, educators, marketers, and agent users can turn scripts, Markdown, or raw text into editable narrated animation projects for knowledge explainers, product introductions, tutorial steps, subtitle-forward videos, and data storytelling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a local Node, Playwright, and ffmpeg toolchain for preview and export. <br>
Mitigation: Install and run it only in an environment where that local media toolchain is acceptable, and use preview mode before export. <br>
Risk: Cloud TTS configuration can use third-party voice synthesis providers and store a provider key locally. <br>
Mitigation: Configure TTS only with an API key approved for that provider, confirm provider and voice before synthesis, and remove ~/.codex/motion-video-skill/secrets.json when the saved key should no longer be retained. <br>
Risk: MP4 export can create rendered media files from the project. <br>
Mitigation: Export only after explicit user confirmation and review the generated preview before running export commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mr-q526/motion-video-skill) <br>
- [Movie Schema](references/movie-schema.md) <br>
- [Animation Rules](references/animation-rules.md) <br>
- [Template Catalog](references/template-catalog.md) <br>
- [TTS Catalog](references/tts-catalog.md) <br>
- [Prompt Patterns](references/prompt-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, code, shell commands, files] <br>
**Output Format:** [Markdown guidance with shell commands plus generated movie.json, preview HTML, optional audio tracks, and confirmed MP4 export files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preview projects use structured movie.json data, 16:9 1280 x 720 scenes, narration-derived timing, optional user-confirmed TTS, and export confirmation before MP4 generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
