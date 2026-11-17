## Description:

HeyVideoGen helps agents produce short-form MP4 videos by planning storyboards, generating TTS and MiniMax Hailuo clips, composing HyperFrames HTML/GSAP scenes, and rendering or post-processing with HyperFrames and FFmpeg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devioslang](https://clawhub.ai/user/devioslang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-automation agents use this skill to turn a video topic or existing HyperFrames project into a storyboard, narration, AI video clips, HTML composition guidance, render commands, and publishable vertical MP4 outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that ordinary video inputs can reach unsafe local command execution paths.

Mitigation: Review and constrain the runner before installation; replace shell=True subprocess calls with argument-list invocations and validate project names, paths, prompts, and output locations.

Risk: The skill orchestrates local rendering, media generation, and file writes through external tools such as HyperFrames, MiniMax scripts, and FFmpeg.

Mitigation: Run the workflow in a sandbox with only the intended workspace and API credentials exposed, and review generated commands before execution.

Risk: Dependency and tool behavior may vary because HyperFrames and related media-generation dependencies are invoked from the local environment.

Mitigation: Pin and review HyperFrames, MiniMax, FFmpeg, and supporting dependencies before production use.

## Reference(s):

- [HyperFrames HTML Authoring](references/html-authoring.md)
- [GSAP Animation Rules](references/gsap-rules.md)
- [Captions & Subtitles](references/captions.md)
- [Scene Transitions](references/transitions.md)
- [TTS & Audio](references/tts.md)
- [Storyboard Example](examples/storyboard-example.json)
- [Apple-Style HyperFrames Template](templates/apple-style/index.html)
- [HyperFrames GitHub Repository](https://github.com/heygen-com/hyperframes)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON storyboard structures, HTML/GSAP examples, Python and shell commands, and file layout instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow targets vertical short-video production and can produce storyboard JSON, HyperFrames HTML compositions, TTS audio, AI video clips, and rendered MP4 files when the required local tools and API credentials are available.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
