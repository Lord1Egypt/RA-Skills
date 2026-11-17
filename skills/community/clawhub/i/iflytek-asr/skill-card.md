## Description:

Converts local audio or downloaded YouTube media to transcripts with the iFlytek ASR API, including Chinese dialect recognition and punctuation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harven-droid](https://clawhub.ai/user/harven-droid)

### License/Terms of Use:

MIT

## Use Case:

Developers and end users use this skill to transcribe meetings, interviews, video audio, voice notes, or YouTube media into text using iFlytek ASR. It is useful when Chinese dialect recognition, punctuation, and file-based transcription are needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The YouTube downloader weakens HTTPS safety.

Mitigation: Remove the downloader certificate-bypass option before use and rely on normal TLS certificate validation.

Risk: The YouTube downloader can be steered to non-YouTube hosts.

Mitigation: Tighten URL validation to canonical YouTube hosts before passing user-supplied URLs to yt-dlp.

Risk: Selected audio or downloaded YouTube media is uploaded to iFlytek, and iFlytek API credentials are stored in a local .env file.

Mitigation: Use only media approved for third-party processing, keep credentials local and unshared, and exclude .env from packages and repositories.

Risk: Dependencies are specified with lower bounds rather than pinned versions.

Mitigation: Install in an isolated virtual environment and pin or lock dependency versions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harven-droid/skills/iflytek-asr)
- [iFlytek Open Platform](https://www.xfyun.cn)
- [iFlytek ASR LLM API documentation](https://www.xfyun.cn/doc/spark/asr_llm/Ifasr_llm.html)
- [iFlytek console](https://console.xfyun.cn)

## Skill Output:

**Output Type(s):** [text, files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; runtime scripts produce transcript text and .txt files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided iFlytek API credentials and network access for API transcription; YouTube workflows also require yt-dlp.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
