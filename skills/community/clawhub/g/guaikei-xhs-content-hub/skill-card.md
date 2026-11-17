## Description:

Searches public Xiaohongshu notes, retrieves note details and comments, and collects creator posts as structured data for content research, competitor analysis, KOL screening, and comment insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, brand marketers, market analysts, MCN teams, and developers use this skill to collect public Xiaohongshu search results, note details, comments, and creator posts for trend research, competitive monitoring, KOL screening, and comment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, links, fetched public data, and an API token to Guaikei, with the token included in request URL parameters.

Mitigation: Use a dedicated, revocable GUAIKEI_API_TOKEN and only submit public Xiaohongshu links or keywords that are approved for third-party processing.

Risk: The skill automatically saves complete command results to local log files.

Mitigation: Run it in a controlled workspace, avoid shared or synced directories for sensitive research, and delete generated logs when retention is not needed.

Risk: The scanner verdict is suspicious because of token handling and local result persistence.

Mitigation: Review the skill and deployment environment before use, and confirm that data-sharing, logging, and retention practices match the user's policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-content-hub)
- [Guaikei API token and support](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, JSON, Guidance]

**Output Format:** [Markdown guidance with Node.js command examples and structured JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require GUAIKEI_API_TOKEN and may save full JSON results under a local logs directory.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
