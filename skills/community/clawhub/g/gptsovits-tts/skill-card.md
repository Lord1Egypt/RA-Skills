## Description: <br>
High-quality Chinese TTS using GPT-SoVITS v2 Pro+ - convert text to natural-sounding speech with voice cloning support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huizong-cpu](https://clawhub.ai/user/huizong-cpu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation builders use this skill to synthesize Chinese speech from text through a local GPT-SoVITS API, including voice cloning with authorized reference audio. It is intended for voice response automation, content narration, and AI voice application workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MP3 conversion path has a command-injection risk when output paths are user-controlled. <br>
Mitigation: Do not pass user-controlled output paths until the ffmpeg call is changed to a safer argument-array API such as execFile or spawn with path validation. <br>
Risk: Voice cloning and TTS requests may expose reference audio or sensitive text to the configured GPT-SoVITS endpoint. <br>
Mitigation: Use only reference audio you have permission to clone and avoid sensitive text unless you trust the configured GPT-SoVITS endpoint. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/huizong-cpu/gptsovits-tts) <br>
- [Publisher profile](https://clawhub.ai/user/huizong-cpu) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, API Calls] <br>
**Output Format:** [MP3 audio file with returned output path string] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configurable TTS sampling parameters and returns a generated MP3 path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
