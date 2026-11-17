## Description:

Write film reviews, get recommendations, and manage watchlists with spoiler control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to draft, revise, optimize, schedule, search, and export movie-review content and related social posts through a local command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Review text and command inputs are saved locally and may be included in exports.

Mitigation: Avoid entering secrets, embargoed drafts, or private material unless you are prepared to manage or delete the files under ~/.local/share/movie-review.

Risk: CSV and JSON exports may contain unescaped special characters from saved entries.

Mitigation: Review and sanitize exported files before sharing them or loading them into downstream tools.

Risk: The advertised scope is broader than the implemented local logging behavior.

Mitigation: Validate that the command output meets the intended review-writing workflow before relying on it for recommendations, spoiler handling, or publishing decisions.

## Reference(s):

- [Movie Review Skill Page](https://clawhub.ai/bytesagain3/skills/movie-review)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Command-line text output with optional JSON, CSV, or plain text export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores timestamped local logs under ~/.local/share/movie-review and can export accumulated entries.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
