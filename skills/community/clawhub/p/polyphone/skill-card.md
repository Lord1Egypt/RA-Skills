## Description:

Helps agents detect Chinese polyphonic characters in TTS text, confirm intended pinyin readings, and synthesize audio with SenseAudio dictionary annotations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and content teams use this skill when generating Chinese TTS with SenseAudio and need to identify, confirm, and apply pinyin overrides for polyphonic characters before synthesis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell example can handle user-provided text unsafely if the request body is assembled by direct string interpolation.

Mitigation: Construct the SenseAudio API payload with a JSON tool or temporary JSON file before invoking curl.

Risk: The skill depends on an external SenseAudio service and a SenseAudio API key.

Mitigation: Install only when the service is trusted for the intended TTS workflow and keep SENSEAUDIO_API_KEY scoped to those requests.

Risk: The broad trigger language may route unrelated pronunciation requests to this skill.

Mitigation: Use it only for intended Chinese TTS polyphone correction tasks that require pinyin dictionary annotations.

## Reference(s):

- [Polyphone TTS on ClawHub](https://clawhub.ai/scikkk/skills/polyphone)
- [SenseAudio homepage](https://senseaudio.cn)
- [SenseAudio API key page](https://senseaudio.cn/platform/api-key)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON dictionary entries and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce SenseAudio API request guidance and an output.mp3 file when the generated commands are executed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
