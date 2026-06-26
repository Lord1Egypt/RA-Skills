## Description: <br>
Transcribes speech from YouTube videos or audio URLs into text using the Gladia API with up to 10 free hours of monthly transcription. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kanfred](https://clawhub.ai/user/kanfred) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to transcribe public or authorized video and audio URLs, including YouTube videos, podcasts, and media files, so the transcript can be reviewed or summarized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The media URL and resulting transcript are sent to Gladia under the user's account. <br>
Mitigation: Use only public or authorized media and avoid submitting content whose transcript should not be processed by Gladia. <br>
Risk: Persisting GLADIA_API_KEY in shell startup files can expose the credential through backups, shared machines, or accidental commits. <br>
Mitigation: Set GLADIA_API_KEY only for the current session or store it in a proper secrets manager. <br>
Risk: The optional output file argument can overwrite an existing file. <br>
Mitigation: Choose transcript output paths deliberately and review the target path before running the script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kanfred/gladia-youtube-transcribe) <br>
- [Publisher profile](https://clawhub.ai/user/kanfred) <br>
- [Gladia](https://gladia.io) <br>
- [Gladia dashboard](https://app.gladia.io) <br>
- [Gladia usage API](https://api.gladia.io/v2/usage) <br>
- [Gladia pre-recorded transcription API](https://api.gladia.io/v2/pre-recorded) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text transcript with Markdown setup and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GLADIA_API_KEY, curl, and python3; can print the transcript to stdout or write it to a caller-provided output file.] <br>

## Skill Version(s): <br>
1.0.4 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
