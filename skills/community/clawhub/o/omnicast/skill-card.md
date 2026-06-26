## Description: <br>
Omnicast is a local multi-modal podcast pipeline that ingests media, drafts scripts, synthesizes audio, renders cover art, packages social media assets, and supports YouTube uploads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaudata](https://clawhub.ai/user/kaudata) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, producers, and developers use Omnicast locally to turn URLs, uploaded files, YouTube transcripts, PDFs, audio, video, and text into podcast scripts, synthesized audio, cover art, LinkedIn assets, and YouTube draft uploads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted media, extracted text, transcripts, scripts, captions, and prompts may be sent to external AI providers. <br>
Mitigation: Use trusted provider accounts and avoid confidential or regulated content unless the relevant provider agreements and data handling requirements allow it. <br>
Risk: Session-management actions can delete saved local session folders. <br>
Mitigation: Keep backups of session folders before using delete-current or delete-all session controls. <br>
Risk: URL ingestion sends user-supplied URLs through the local processing pipeline. <br>
Mitigation: Review URLs before ingestion and run the service on a trusted local machine. <br>


## Reference(s): <br>
- [Omnicast ClawHub listing](https://clawhub.ai/kaudata/omnicast) <br>
- [kaudata publisher profile](https://clawhub.ai/user/kaudata) <br>
- [README](README.md) <br>
- [SKILL](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Audio files, Image files, Video files, JSON] <br>
**Output Format:** [Local web application and API outputs including text, JSON responses, generated media files, downloadable archives, and setup commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local API keys for Gemini and OpenAI, optional provider credentials for additional services, and FFmpeg for audio and video processing.] <br>

## Skill Version(s): <br>
1.0.14 (source: server release metadata; package.json reports 1.0.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
