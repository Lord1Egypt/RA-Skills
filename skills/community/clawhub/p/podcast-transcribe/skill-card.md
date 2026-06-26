## Description: <br>
For transcript or subtitle requests involving podcast URLs, public audio URLs/files, or raw transcript cleanup. Generates audio + SRT + TXT artifacts and can optionally clean transcripts with episode-page context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dairui1](https://clawhub.ai/user/dairui1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content teams use this skill to transcribe podcast episodes, public audio URLs, or local audio files into audio, SRT, and TXT artifacts. They can optionally request conservative transcript cleanup using episode-page context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow runs an external podcast-helper package and may process audio with configured cloud transcription providers. <br>
Mitigation: Install only when the external CLI is acceptable, review provider selection before execution, and choose the local mlx-whisper engine for sensitive recordings. <br>
Risk: Provider API keys may be required for hosted transcription engines. <br>
Mitigation: Confirm only the needed provider key is set and avoid printing, logging, or sharing full API keys. <br>
Risk: Optional cleanup can fetch episode-page context through Jina Reader, which may expose private or sensitive URLs. <br>
Mitigation: Use cleanup context only for public episode pages and skip Jina cleanup context for private URLs. <br>
Risk: Transcript cleanup can accidentally change meaning if the model fills gaps or over-edits ASR output. <br>
Mitigation: Keep the raw transcript unchanged, write cleanup to a sibling file, and limit edits to obvious ASR repairs, punctuation, paragraphing, and proper nouns supported by context. <br>


## Reference(s): <br>
- [Inputs and Engines](references/inputs-and-engines.md) <br>
- [Output Contract](references/output-contract.md) <br>
- [Cleanup Guidance](references/cleanup.md) <br>
- [Verification](references/verification.md) <br>
- [Setup](references/setup.md) <br>
- [ClawHub skill page](https://clawhub.ai/dairui1/podcast-transcribe) <br>
- [Publisher profile](https://clawhub.ai/user/dairui1) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands, JSON envelopes, and generated audio, SRT, TXT, and cleaned TXT file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers machine-readable JSON output from podcast-helper and may emit JSONL progress events on stderr.] <br>

## Skill Version(s): <br>
1.4.1 (source: server evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
