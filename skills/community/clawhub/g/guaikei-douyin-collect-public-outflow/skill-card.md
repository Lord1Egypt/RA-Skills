## Description:

This skill helps agents collect public Douyin search results, creator posts, video comments, and trending topics as structured JSON for short-video research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content analysts use this skill to gather public Douyin data for keyword research, competitor monitoring, comment analysis, and trending-topic tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API token is sent to the Guaikei API and may be exposed through service logs.

Mitigation: Use a scoped token where possible, keep it out of shared transcripts and files, and rotate it after use or suspected exposure.

Risk: Collected public Douyin comments, account metadata, and search results are saved locally by default.

Mitigation: Review the logs directory after each run and delete files that contain data you do not want retained.

Risk: The security summary reports a mismatch between promised neutral authentication errors and observed behavior.

Mitigation: Review the skill before installation and stop on authentication errors instead of retrying or following unexpected promotional guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-collect-public-outflow)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Repository metadata](https://github.com/um-why/douyin-search-openclaw)
- [README](artifact/readme.md)
- [Options reference](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Files, Shell commands, Guidance]

**Output Format:** [Structured JSON on stdout, JSON log files, and concise agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a GUAIKEI_API_TOKEN; collected public data is saved under the skill logs directory by default.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json, changelog, and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
