## Description: <br>
Transcribes audio, generates subtitles, or translates speech through a self-hosted Whisper ASR service running on Kubernetes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xavjer](https://clawhub.ai/user/Xavjer) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators with access to the Kubernetes Whisper service use this skill to convert audio files into transcripts, subtitle files, JSON output, or English translations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A crafted prompt can execute local Python code through the artifact's prompt handling. <br>
Mitigation: Patch prompt URL encoding to avoid shell-interpreted interpolation, and avoid untrusted prompt text until the script is fixed. <br>
Risk: Audio is sent to an unauthenticated HTTP Whisper service. <br>
Mitigation: Use only on trusted Kubernetes networks, avoid sensitive audio when plain HTTP and no authentication are unacceptable, and add transport protection or authentication before broader deployment. <br>


## Reference(s): <br>
- [Whisper ASR Webservice](https://github.com/ahmetoner/whisper-asr-webservice) <br>
- [Internal Whisper ASR Swagger Docs](http://whisper-asr.whisper-asr.svc.cluster.local:9000/docs) <br>
- [ClawHub Release Page](https://clawhub.ai/Xavjer/openclaw-self-hosted-whisper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Configuration] <br>
**Output Format:** [Plain text, JSON, WebVTT, SRT, or TSV transcript files with terminal status messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and network access to the internal Kubernetes Whisper ASR endpoint; no authentication is configured in the artifact.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
