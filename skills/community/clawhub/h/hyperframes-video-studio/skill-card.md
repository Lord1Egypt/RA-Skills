## Description: <br>
Guided OpenClaw video studio for Hyperframes: templates, safety audit, local-first TTS, and renderable HTML projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, and developers use this skill to turn briefs and existing materials into template-based Hyperframes HTML video projects with guided prompts, asset intake, narration, and render preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected-file ingestion and generated project data can cache file metadata, text excerpts, audio, and render outputs. <br>
Mitigation: Use narrow asset folders, avoid sensitive source material when possible, and review or delete .cache after sensitive projects. <br>
Risk: Edge-TTS is a zero-cost, keyless fallback that uses remote processing for narration text. <br>
Mitigation: Use local Piper TTS for confidential narration, or use Edge-TTS only when remote text processing is acceptable. <br>
Risk: The optional Hyperframes install can fetch an npm package into the skill cache. <br>
Mitigation: Confirm installation only when the Hyperframes package source is trusted; the documented install path is local to .cache and does not require sudo or global PATH changes. <br>


## Reference(s): <br>
- [Hyperframes upstream repository](https://github.com/heygen-com/hyperframes) <br>
- [ClawHub skill page](https://clawhub.ai/tobewin/hyperframes-video-studio) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request shapes, bash commands, and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates manifests and renderable HTML project files under .cache; rendering and dependency installation require confirmation.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
