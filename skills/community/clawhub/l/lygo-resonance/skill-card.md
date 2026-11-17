## Description:

LYGO RESONANCE transforms images into stereo soundscapes, creative JSON profiles, AI-ready music and lyric briefs, video-driven audio, and local LLM lyric drafts using computer-vision-driven analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

Artists, musicians, creative developers, and agents use this skill to turn local images or videos into generated WAV soundscapes, musical DNA profiles, creative briefs, MIDI/stem exports, and lyric drafts. It can also guide interactive or batch use through the included Gradio interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes publishing, token-loading, memory-update, and external-posting guidance that could affect accounts or persistent state if followed uncritically.

Mitigation: Treat those maintenance and publishing steps as out of scope unless the user explicitly authorizes them for this release.

Risk: Batch image, video, or brief processing can create many local files or send brief text to a configured local LLM endpoint.

Mitigation: Run in a dedicated project folder or virtual environment, confirm batch inputs and outputs before execution, and verify the LLM URL before sending briefs.

Risk: Dependency installation and script execution may change the local Python environment.

Mitigation: Use a dedicated virtual environment and pinned dependencies where possible before running the modules.

## Reference(s):

- [LYGO RESONANCE live site](https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html)
- [LYGO RESONANCE alternate site](https://deepseekoracle.github.io/Excavationpro/LYGO-Resonance/)
- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/lygo-resonance)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and references to generated files such as WAV, JSON, MID, TXT, and optional Gradio outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or reference local audio, profile, MIDI, brief, lyric, and manifest files when the agent runs the bundled scripts.]

## Skill Version(s):

0.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
