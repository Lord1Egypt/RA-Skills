## Description: <br>
Asset preprocessing for HyperFrames compositions: text-to-speech narration with Kokoro, audio/video transcription with Whisper, and background removal for transparent overlays with u2net. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucas-kay8](https://clawhub.ai/user/lucas-kay8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and media-focused agents use this skill to generate local narration, create word-level transcripts for captions, and prepare transparent foreground or layer assets for HyperFrames compositions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio and video inputs can contain personal or sensitive information. <br>
Mitigation: Review media before processing and handle generated transcripts, narration, and cutouts according to the user's data-handling requirements. <br>
Risk: The workflows invoke npx, Python packages, system packages, and first-run model downloads. <br>
Mitigation: Install from trusted package sources, review dependencies before use, and expect large local model caches under the HyperFrames cache directory. <br>
Risk: Using English-only Whisper models on non-English audio can translate instead of preserving the original language. <br>
Mitigation: Use non-.en Whisper models unless the audio is explicitly English, and pass a language code when the language is known. <br>
Risk: The background plate output is a transparent hole-cut layer, not an inpainted clean plate. <br>
Mitigation: Use the plate only for layered compositions; choose an inpainting tool when a standalone room or background with the subject removed is required. <br>


## Reference(s): <br>
- [Hyperframes Media on ClawHub](https://clawhub.ai/lucas-kay8/hyperframes-media) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash commands, tables, and JSON/HTML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides local CLI workflows that can produce audio, transcript JSON, transparent video, MOV, PNG, and cached model files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
