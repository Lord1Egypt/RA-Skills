## Description:

Kmoe manga downloader that helps agents search Kmoe manga, download selected volumes, manage credential pools, and report download progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrisis58](https://clawhub.ai/user/chrisis58)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate the kmdr CLI for finding Kmoe manga, estimating quota impact, starting downloads, and checking background-download progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation instructions use a mutable pre-release downloader package range.

Mitigation: Install in an isolated environment and pin or review the exact kmoe-manga-downloader version before use.

Risk: Password-based login can expose credentials if the agent receives or runs the password in chat or command arguments.

Mitigation: Prefer user-run terminal login and avoid sending passwords through chat, transcripts, or command history.

Risk: Downloads can consume account quota or save files to an unintended destination.

Mitigation: Use explain, status, and config checks before starting a background download.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chrisis58/skills/kmdr)
- [Kmoe](https://kxx.moe/)
- [Output Format](references/output-format.md)
- [Error Codes](references/error-codes.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown, JSON]

**Output Format:** [Markdown guidance with inline shell commands and NDJSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [kmdr toolcall mode emits result and progress JSON objects; background downloads return a task_id for later progress checks.]

## Skill Version(s):

1.0.0-a4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
