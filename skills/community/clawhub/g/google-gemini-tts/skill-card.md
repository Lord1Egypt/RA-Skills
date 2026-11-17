## Description:

Generate spoken audio from text using Google's Gemini TTS models (default is Gemini 3.1 Flash TTS Preview, with fallback to Gemini 2.5 Flash/Pro preview TTS).

This skill is ready for commercial/non-commercial use.

## Publisher:

[shubhamsaboo](https://clawhub.ai/user/shubhamsaboo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn generated text into WAV speech for voice replies, briefings, narration, podcast-style two-speaker conversations, and style-controlled spoken output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-provided text, style prompts, and related request data to Google's Gemini API.

Mitigation: Use it only for data your policy permits sending to Gemini, and avoid secrets, regulated data, or private documents unless approved.

Risk: Gemini API usage may consume quota or incur billing, especially when preview models are selected.

Mitigation: Monitor Google API quota and billing for the API key used by the agent.

Risk: Preview model names may change or be retired.

Mitigation: Check the current Gemini model list and use the documented fallback model option when needed.

## Reference(s):

- [Gemini speech generation documentation](https://ai.google.dev/gemini-api/docs/speech-generation)
- [Gemini model list](https://ai.google.dev/gemini-api/docs/models)
- [Google AI Studio API key setup](https://aistudio.google.com/apikey)
- [ClawHub skill page](https://clawhub.ai/shubhamsaboo/skills/google-gemini-tts)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Audio files, Guidance]

**Output Format:** [Markdown guidance with shell commands; the runtime script writes a local WAV file path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 24 kHz mono, 16-bit PCM WAV output after converting Gemini audio response data with ffmpeg.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
