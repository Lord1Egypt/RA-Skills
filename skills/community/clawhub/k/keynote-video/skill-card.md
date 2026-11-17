## Description:

Keynote Video converts presentation decks into narrated videos by guiding an agent through input review, script generation, style selection, user approval, text-to-speech assembly, video composition, and quality checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentlau2046-sudo](https://clawhub.ai/user/vincentlau2046-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Presentation creators, developers, and content teams use this skill to turn PPT, PPTX, or PDF presentations plus optional background material into spoken video drafts. It helps an agent evaluate inputs, write plain-text narration scripts, prepare a video design spec for user approval, run synthesis commands, and report video quality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generator can run unsafe shell commands from user-controlled presentation paths or generated spec values.

Mitigation: Use only trusted presentation paths and trusted generated specs in an isolated workspace; replace shell-string execSync calls with argument-array process APIs before broader deployment.

Risk: Narration text may be sent to the edge-tts provider during speech synthesis.

Mitigation: Do not process confidential decks unless users have accepted cloud TTS disclosure and data handling requirements.

Risk: Voice and rate values from generated specs can influence command execution behavior.

Mitigation: Validate voice and rate values against an allowlist before invoking synthesis commands.

Risk: Unpinned runtime dependencies and external tools can change behavior across environments.

Mitigation: Pin Node, Python, ffmpeg, LibreOffice, edge-tts, and related package versions for repeatable releases.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vincentlau2046-sudo/skills/keynote-video)
- [README.md](artifact/README.md)
- [DESIGN.md](artifact/DESIGN.md)
- [Video Design Spec Template](artifact/templates/video_design_spec_template.md)
- [Script Page Template](artifact/templates/script_page_template.md)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown workflow guidance, plain-text narration scripts, JSON video design specs, shell commands, MP4 video files, and Markdown completion reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before video synthesis; generated media depends on local tools and cloud text-to-speech availability.]

## Skill Version(s):

2.1.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
