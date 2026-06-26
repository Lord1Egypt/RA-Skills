## Description: <br>
Generate spoken audio from text using Google's Gemini TTS models for voice replies, narrated briefings, podcast-style two-speaker conversations, expressive delivery, and WAV output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shubhamsaboo](https://clawhub.ai/user/shubhamsaboo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert text into Gemini-generated speech, including single-speaker narration, two-speaker dialogue, style-controlled voice output, and WAV files for voice-enabled workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for speech generation and the Gemini API key are sent to Google's API. <br>
Mitigation: Use the skill only with text appropriate for Google processing, trust the publisher before installing, and prefer a dedicated GEMINI_API_KEY with limited exposure. <br>
Risk: The script can create the selected output directory and overwrite the chosen WAV file path. <br>
Mitigation: Choose output paths deliberately and avoid pointing the output option at important existing files. <br>
Risk: Preview model names may change or be retired. <br>
Mitigation: Use the documented fallback model option or check the current Gemini model list before relying on a model name in production workflows. <br>


## Reference(s): <br>
- [Gemini speech generation documentation](https://ai.google.dev/gemini-api/docs/speech-generation) <br>
- [Gemini model list](https://ai.google.dev/gemini-api/docs/models) <br>
- [Google AI Studio API key setup](https://aistudio.google.com/apikey) <br>
- [ClawHub skill page](https://clawhub.ai/shubhamsaboo/google-gemini-tts) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; runtime output is a WAV file path and generated audio file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GEMINI_API_KEY or GOOGLE_API_KEY and host tools curl, jq, base64, and ffmpeg.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
