## Description: <br>
Generates professional voiceover narration for videos with audio-video sync using text-to-speech tooling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[feiskyer](https://clawhub.ai/user/feiskyer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and technical content teams use this skill to analyze a video, write or refine timed narration, synthesize voice audio, and merge it into a synchronized narrated video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local API key handling for text-to-speech services can expose credentials if values are printed, committed, or shared. <br>
Mitigation: Store credentials in the configured local environment file, check only for their presence, and never display secret values. <br>
Risk: Broad activation wording may trigger the skill for requests involving music, sound effects, or unrelated audio editing. <br>
Mitigation: Clarify ambiguous audio requests before generating narration or modifying a video. <br>
Risk: Text submitted for speech synthesis may be sent to an external text-to-speech provider. <br>
Mitigation: Avoid submitting sensitive text unless the user accepts the provider data-handling implications. <br>


## Reference(s): <br>
- [Azure TTS Voice Reference](references/voices.md) <br>
- [ClawHub skill page](https://clawhub.ai/feiskyer/narrate-video) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with Python configuration and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce a configured narration script, generated audio segments, and a narrated video file when executed by the agent.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
