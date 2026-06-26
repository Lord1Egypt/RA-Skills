## Description: <br>
Fix Chinese polyphone mispronunciation in TTS by detecting ambiguous characters, asking the user to confirm pronunciations, and applying pinyin annotations for SenseAudio synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scikkk](https://clawhub.ai/user/scikkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and TTS operators use this skill to improve Chinese pronunciation in SenseAudio text-to-speech workflows, especially for ambiguous polyphonic characters. It helps build and apply pinyin dictionary entries before synthesizing speech with a cloned voice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The synthesized text and selected cloned voice ID are sent to SenseAudio. <br>
Mitigation: Avoid submitting sensitive or confidential text unless SenseAudio's terms and data handling are acceptable for the user's use case. <br>
Risk: The workflow requires a SenseAudio API key and a cloned voice. <br>
Mitigation: Protect the SENSEAUDIO_API_KEY and use only voices the user is authorized to use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scikkk/polyphone) <br>
- [SenseAudio homepage](https://senseaudio.cn) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON dictionary examples and bash command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce confirmed pinyin dictionary entries, SenseAudio API request guidance, and an output audio file path after synthesis.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
