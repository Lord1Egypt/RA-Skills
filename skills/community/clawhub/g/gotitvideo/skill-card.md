## Description:

Converts local video files or public video links into cleaned transcription text, summaries, meeting notes, subtitles, rewrites, quotes, translations, and other prompt-guided content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content teams use this command skill to turn videos or audio-heavy recordings into usable text outputs such as transcripts, summaries, meeting minutes, subtitles, social posts, quotes, and translations. Developers and agents can call the Node.js command with a file, URL, task ID, and optional prompt to produce a single text result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected videos, prompts, task IDs, API tokens, and file metadata may be sent to third-party services.

Mitigation: Use only with media approved for that provider, avoid confidential or regulated content, and confirm the provider's retention and handling policy before use.

Risk: The skill can fetch arbitrary user-provided URLs before upload.

Mitigation: Avoid internal-network, localhost, metadata-service, authenticated, access-restricted, or copyright-sensitive URLs; prefer vetted public links or local files.

Risk: Generated transcripts, summaries, and rewrites may be inaccurate for noisy audio, overlapping speakers, strong accents, or specialized subject matter.

Mitigation: Review outputs manually before publication or decision-making, especially for legal, medical, financial, or regulated content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/gotitvideo)
- [GuaiKei service website](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or prompt-shaped text emitted on stdout; documentation examples use Markdown with inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and GUAIKEI_API_TOKEN. Outputs depend on the supplied video, task ID, and optional prompt.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
