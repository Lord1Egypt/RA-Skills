## Description: <br>
Music composition assistant that guides users through genre, mood, theme, tempo, and other musical choices, generates structured Suno or Udio prompts, and can save generated audio to a user-specified path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gentleyo](https://clawhub.ai/user/gentleyo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to turn a natural-language music idea into structured prompt variants for Suno or Udio, with optional guidance for web-based or local automated generation. It also helps collect generation settings such as genre, mood, tempo, instrumentation, vocals, duration, and output path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional API automation depends on unofficial community wrappers and may break when Suno or Udio change their services. <br>
Mitigation: Use the web interface path when prompt generation is sufficient, and review the wrapper project status before enabling automation. <br>
Risk: Automation may require account session credentials and a SUNO_API_URL endpoint. <br>
Mitigation: Keep credentials out of shared files, configure them only in the trusted local service, and point SUNO_API_URL only at a trusted endpoint. <br>
Risk: Generated music may be subject to Suno or Udio platform terms before commercial use. <br>
Mitigation: Review the selected platform's terms of service before distributing or monetizing generated audio. <br>
Risk: Generated audio files are written to a user-selected output directory. <br>
Mitigation: Use a dedicated output folder and confirm the path before running automated generation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gentleyo/music-generate) <br>
- [Suno](https://suno.com) <br>
- [Udio](https://www.udio.com) <br>
- [Community Suno API wrapper](https://github.com/gcui-art/suno-api) <br>
- [Community Udio API wrapper](https://github.com/udioapi/udio-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with structured prompt options, setup guidance, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save generated MP3 files to a user-specified folder when configured with a trusted local API service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
