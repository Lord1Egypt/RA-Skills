## Description: <br>
OpenAI Text-to-Speech API for high-quality speech synthesis with customizable voices and tone control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lnj22](https://clawhub.ai/user/lnj22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use this skill to generate natural-sounding speech from text with OpenAI TTS, including audiobook-style audio from longer documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OpenAI API key, which is sensitive credential material. <br>
Mitigation: Provide the key through the OPENAI_API_KEY environment variable and avoid placing it in prompts, source files, logs, or generated audio-processing scripts. <br>
Risk: Generated speech can misrepresent written content if text chunking, tone instructions, or concatenation are reviewed poorly. <br>
Mitigation: Review the input text, selected voice, tone instructions, and final audio before publishing or distributing generated audiobook files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lnj22/pg-essay-to-audiobook-openai-tts) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce code that reads OPENAI_API_KEY and writes audio files such as MP3 or WAV.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
