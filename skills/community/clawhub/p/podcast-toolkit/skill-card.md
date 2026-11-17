## Description:

播客 helps agents plan podcast episodes, draft scripts and show notes, suggest audio and video post-production commands, and prepare social clips and distribution copy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, podcast producers, and developer-led media teams use this skill to plan podcast series, draft episode scripts and show notes, prepare post-production guidance, and package short clips for distribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example media commands can operate on the wrong local file or overwrite an intended output.

Mitigation: Use trusted local media paths, review input and output filenames before execution, and keep backups of source recordings.

Risk: Podcast workflows can accidentally process or distribute copyrighted media without permission.

Mitigation: Use original or properly licensed audio and video, and verify rights before editing, clipping, or publishing.

Risk: API keys or service credentials used with supporting tools can be exposed in project files.

Mitigation: Store credentials in environment variables and avoid committing keys, transcripts, or private media paths to version control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/podcast-toolkit)
- [FFmpeg downloads](https://ffmpeg.org/download.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON-shaped examples with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include podcast episode plans, scripts, show notes, clip timestamps, SEO copy, media processing parameters, and command examples.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
