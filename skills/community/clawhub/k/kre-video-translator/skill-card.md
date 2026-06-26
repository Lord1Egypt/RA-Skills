## Description: <br>
Translate local audio or video files into multilingual .srt subtitles with KreTrans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skz7s](https://clawhub.ai/user/skz7s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to translate local audio or video files into subtitle files, including workflows where a URL or magnet source is downloaded first and then processed as a local media file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected media audio, filenames, and language settings are sent to KreTrans for translation. <br>
Mitigation: Use a revocable KreTrans API key and avoid highly sensitive recordings unless the user trusts the service. <br>
Risk: URL or magnet inputs require external download tools before translation. <br>
Mitigation: Confirm the source and download tooling before processing, or ask the user to provide a local media file instead. <br>


## Reference(s): <br>
- [Setup](references/setup.md) <br>
- [KreTrans Homepage](https://kretrans.com) <br>
- [KreTrans API Documentation](https://kretrans.com/api-docs) <br>
- [KreTrans API Key Management](https://kretrans.com/console#api-management) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands and generated .srt subtitle files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates one primary .srt subtitle output for the selected target language; translation jobs are asynchronous and require KRETRANS_API_KEY, ffmpeg, Python, and requests.] <br>

## Skill Version(s): <br>
1.0.3 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
