## Description: <br>
Create audiobooks from web content or text files. Handles content fetching, text processing, and TTS conversion with automatic fallback between ElevenLabs, OpenAI TTS, and gTTS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lnj22](https://clawhub.ai/user/lnj22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to turn web articles, essays, or text files into audiobook workflows with content fetching, text cleanup, TTS provider selection, and audio concatenation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text converted by the workflow may be sent to external TTS providers, including Google-backed gTTS when no API key is used. <br>
Mitigation: Avoid confidential, regulated, or sensitive internal content unless the selected provider terms and organizational policies allow it. <br>
Risk: Paid TTS providers require API keys and may incur usage costs. <br>
Mitigation: Use API keys intended for this task, keep credentials scoped appropriately, and confirm cost controls before running conversions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lnj22/pg-essay-to-audiobook-audiobook) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes environment-variable based provider selection and example workflows that can create MP3 audiobook files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
