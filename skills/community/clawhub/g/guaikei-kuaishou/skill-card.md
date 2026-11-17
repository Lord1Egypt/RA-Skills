## Description:

Guaikei Kuaishou helps agents search public Kuaishou videos by keyword, list public creator posts, and retrieve video comments as structured JSON for content research, competitor monitoring, KOL screening, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content teams, marketers, MCN operators, and analysts use this skill to collect public Kuaishou search results, creator posts, and video comments for topic research, competitor monitoring, KOL screening, sentiment review, and trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kuaishou keywords, profile or video identifiers, and GUAIKEI_API_TOKEN are sent to the third-party guaikei.com service.

Mitigation: Use the skill only when the user is comfortable with that data flow, keep the token in environment configuration, and rotate or revoke the token if exposure is suspected.

Risk: Fetched comments, creator data, and business research can remain on disk in local log files.

Mitigation: Review and delete logs that contain sensitive research, and avoid committing generated log files to shared repositories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-kuaishou)
- [Guaikei API and token support](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Structured JSON results with concise text summaries and command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes fetched results to local JSON files under logs/ and requires GUAIKEI_API_TOKEN for API access.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json, and changelog; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
