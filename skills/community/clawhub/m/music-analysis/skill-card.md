## Description:

Analyzes local music and audio files to produce tempo, groove, structure, harmony, timbre, instrument, temporal mood, and lyric-aware emotional notes without external APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adam-researchh](https://clawhub.ai/user/adam-researchh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, producers, and audio reviewers use this skill to inspect tracks from local audio files, compare mixes, understand musical structure, and generate producer-facing notes. It is useful when an agent is asked to listen to music, audit a recording, or summarize groove, harmony, timbre, instrumentation, mood, and lyric alignment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private audio or transcribed lyrics may appear in generated reports.

Mitigation: Run the skill only on audio approved for local analysis, and review reports before sharing them outside the workspace.

Risk: Reports can be written to a user-provided output path.

Mitigation: Choose an explicit output location and avoid overwriting unrelated project files.

Risk: Unpinned Python dependencies may produce non-reproducible installs or behavior.

Mitigation: Pin and review Python dependencies before deploying the skill in a shared or production environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/adam-researchh/skills/music-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON music-analysis reports, with optional files written via --out.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are generated from local audio files and may include measured audio features, inferred musical structure, instrument palette notes, timeline highlights, and lyric excerpts when local Whisper transcription is available.]

## Skill Version(s):

3.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
