## Description:

This skill helps agents retrieve public Douyin data for keyword search, creator posts, video comments, and real-time hot topic lists, returning structured JSON for analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to gather public Douyin search results, creator posts, comments, and hot topic data for content research, competitive analysis, marketing reports, and trend monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Douyin search terms, target URLs or identifiers, and GUAIKEI_API_TOKEN to a vendor service.

Mitigation: Use it only when the vendor and retention model are acceptable, avoid confidential research targets, and rotate the token if it may have been exposed.

Risk: Runs may save result data to a local logs directory.

Mitigation: Review and clear logs after use when search targets, URLs, comments, or result records are sensitive.

Risk: Broad activation can collect Douyin data for loosely phrased user requests.

Mitigation: Confirm intent and scope before running commands, especially for large limits or competitive research.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-vault)
- [Complete options](references/options.md)
- [Changelog](references/changelog.md)
- [README](readme.md)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Files]

**Output Format:** [JSON on stdout with JSON log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single runs can request up to 10,000 public Douyin records and may write logs under logs/.]

## Skill Version(s):

1.0.0 (source: package.json, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
