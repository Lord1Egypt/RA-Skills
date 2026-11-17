## Description:

Searches Xiaohongshu notes, retrieves note details and comments, and fetches creator post lists from supported keywords or Xiaohongshu URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content teams, marketers, and data analysts use this skill to collect public Xiaohongshu note, comment, and creator-post data for market research, content planning, KOL screening, and competitive analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaohongshu keywords, note URLs, profile URLs, and the Guaikei API token are sent to www.guaikei.com.

Mitigation: Use the skill only when that data sharing is acceptable, avoid sensitive or long-lived token-bearing URLs, and protect or rotate the API token if exposure is suspected.

Risk: Command results are saved locally under logs/ and may contain returned social data or token-bearing URLs.

Mitigation: Protect generated logs, delete them when no longer needed, and avoid sharing log directories externally.

Risk: The security evidence flags the release as suspicious because credential and token-bearing data handling needs user review.

Mitigation: Review the security guidance before installation and prefer a future version with Authorization-header credentials and log redaction or opt-in logging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-search-results)
- [Guaikei service page](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands; executed CLI commands return structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and GUAIKEI_API_TOKEN; command results are also saved locally under logs/.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
