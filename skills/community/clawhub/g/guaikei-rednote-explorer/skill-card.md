## Description:

Collects public Xiaohongshu/Rednote keyword search results, note details, note comments, and creator posts as structured data for downstream analysis and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, content operators, analysts, and agent developers use this skill to retrieve public Xiaohongshu/Rednote content data before summarizing, comparing, monitoring competitors, screening KOLs, or producing reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a paid API token and may expose sensitive token-related context through terminal sessions or shared artifacts.

Mitigation: Treat GUAIKEI_API_TOKEN as sensitive, avoid sharing terminal output or generated logs, and rotate the token if it was printed or captured.

Risk: Runs can save business research targets and returned public-content data into local JSON logs.

Mitigation: Review whether the targets and results may be stored, share logs only with authorized recipients, and delete generated logs when they are no longer needed.

Risk: The skill depends on the Guaikei API service to retrieve Xiaohongshu/Rednote data.

Mitigation: Review the skill before installing for real business research and confirm that external data transfer and API use fit the user's authorization scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-rednote-explorer)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Guaikei website](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [shell commands, json, guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command output includes status, error_code, request metadata, runtime metadata, and results; successful runs also save JSON result logs.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
