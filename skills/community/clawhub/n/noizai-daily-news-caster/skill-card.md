## Description:

Fetches the latest news using news-aggregator-skill, formats it into a podcast script in Markdown format, and uses the tts skill to generate a podcast audio file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ksuriuri](https://clawhub.ai/user/ksuriuri)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn current news into a concise two-host podcast script and generated audio file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Custom or cloned voice generation can send podcast text and user-provided reference recordings to a third-party TTS service without explicit confirmation.

Mitigation: Confirm the TTS backend before generation, use cloned voices only with authorization from every recorded speaker, and prefer non-cloned guest-mode voices when voice cloning is not required.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown podcast script, command guidance, generated WAV audio files, and a short headline summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates podcast_script.md, line_*.wav, list.txt, and podcast_output.wav in the current working directory.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
