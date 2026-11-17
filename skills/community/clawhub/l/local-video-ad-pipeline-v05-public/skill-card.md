## Description:

Local Video Ad Pipeline v0.5 helps agents plan and run a local GPU workflow for short commercial videos and YouTube Shorts using a local LLM, ComfyUI image and video generation, optional ACE-Step BGM, ffmpeg assembly, and QA scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[k0103292xxxx](https://clawhub.ai/user/k0103292xxxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to direct, generate, assemble, and QA short local-model video advertisements or YouTube Shorts. It is intended for local GPU workflows that need sequential image, video, audio, subtitle, and final MP4 production steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project prompts or media can be sent to configurable ComfyUI or ACE-Step services.

Mitigation: Keep --comfy and --ace endpoints on loopback or trusted HTTPS services, and review project JSON before generation or composition.

Risk: Fallback keyframe helpers can load unpinned external Python modules from a Qwen GUI path.

Mitigation: Use the direct ComfyUI keyframe workflow when possible, and only use the GUI fallback with a known, controlled module path.

Risk: Local operational steps can disrupt running services or expose media through Telegram upload paths.

Mitigation: Require explicit confirmation before WSL shutdown or Telegram upload, and keep bot tokens out of chat logs.

Risk: Default prompt guidance includes Korean adult-glamour casting assumptions.

Mitigation: Override defaults for conservative, minor, school-age, childlike, or age-ambiguous projects and review prompts before generation.

## Reference(s):

- [ACE-Step BGM](references/ace_bgm.md)
- [Character Consistency Workflow](references/character_consistency.md)
- [Expression Language](references/expression_language.md)
- [Pre-production Scripting](references/preproduction.md)
- [Subtitle-Based Variable Timing](references/subtitle_timing.md)
- [Wan2.2 Server Tuning](references/wan22_server.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides creation of project planning JSON, keyframes, video clips, optional BGM, subtitles, contact sheets, validation reports, and final MP4 files through local tools.]

## Skill Version(s):

0.5.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
