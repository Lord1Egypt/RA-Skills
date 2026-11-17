## Description:

Build and operate an automated archive workflow for the Hacker News podcast/feed: detect new episodes from RSS, download audio, transcribe locally with Whisper, generate markdown archives with metadata, and keep an index/history for repeatable ingestion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up or maintain a repeatable RSS podcast archive that downloads episodes, transcribes audio locally, and writes searchable markdown records with state and run history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feed-controlled RSS and enclosure URLs can direct downloads to arbitrary network locations.

Mitigation: Use trusted RSS feeds only, or add allowlisting for expected HTTPS domains and block local or private-network destinations before scheduling recurring runs.

Risk: Large or slow downloads and transcriptions can consume local compute, storage, or network resources.

Mitigation: Add network timeouts and file size limits, and test with --limit or --dry-run before enabling unattended automation.

Risk: Unreviewed dependency changes can alter runtime behavior.

Mitigation: Pin reviewed versions of feedparser and required local binaries in the environment used to run the archive pipeline.

## Reference(s):

- [Archive layout](references/layout.md)
- [OpenClaw automation template](references/openclaw-automation.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown, text]

**Output Format:** [Markdown guidance with shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When run, the bundled script can create local audio files, transcript text files, episode markdown files, index.md, state.json, and run-log.jsonl.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
