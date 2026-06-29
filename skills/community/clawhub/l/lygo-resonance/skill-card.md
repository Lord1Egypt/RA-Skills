## Description: <br>
LYGO RESONANCE transforms images and videos into stereo soundscapes, creative JSON profiles, music briefs, lyrics, MIDI, and local Gradio workflows using computer-vision features and optional local LLM expansion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deepseekoracle](https://clawhub.ai/user/deepseekoracle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Artists, musicians, creators, and agent developers use this skill to convert images or videos into local creative outputs such as WAV soundscapes, musical DNA profiles, AI music prompts, briefs, MIDI, and expanded lyrics. It can be used through command-line scripts or a local Gradio interface for single-file or batch processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can generate multiple WAV, MIDI, JSON, brief, and lyric files during single or batch runs. <br>
Mitigation: Use explicit input and output folders, review disk usage before batch processing, and inspect generated files before sharing or reusing them. <br>
Risk: The local Gradio interface and optional LLM expansion can expose local workflows or send prompts to a configured endpoint. <br>
Mitigation: Launch the UI only when needed and point the LLM URL only at a local or otherwise trusted service. <br>
Risk: Artifact text mentions memory growth, external posting, and publishing workflows. <br>
Mitigation: Treat memory writes, external sharing, and publishing as separate high-impact actions that require direct user approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deepseekoracle/lygo-resonance) <br>
- [Publisher profile](https://clawhub.ai/user/deepseekoracle) <br>
- [LYGO RESONANCE website](https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html) <br>
- [Alternate LYGO Resonance site path](https://deepseekoracle.github.io/Excavationpro/LYGO-Resonance/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, JSON, Audio files, MIDI files] <br>
**Output Format:** [Markdown guidance with shell commands, Python code modules, JSON profiles, text briefs and lyrics, WAV audio files, and optional MIDI files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local file outputs may include WAV, stem WAV, JSON, MID, TXT, and lyrics files; optional LLM expansion calls a configured local endpoint.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
