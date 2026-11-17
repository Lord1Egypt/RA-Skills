## Description:

Provides agent-run commands for Douyin keyword search, hot list lookup, creator post retrieval, and public video comment collection for competitor intelligence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, analysts, and content teams use this skill to collect public Douyin search results, creator posts, comments, and hot-list data for content research, competitor monitoring, sentiment review, and trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts www.guaikei.com with the API token and search targets.

Mitigation: Review the skill before installing, avoid sensitive investigations, and use a token that can be rotated if exposure or URL logging is a concern.

Risk: Collected results are automatically retained locally under logs/ and may include comments or profile data.

Mitigation: Limit collection to what is needed, clear saved logs after use, and avoid retaining personal or sensitive data longer than necessary.

Risk: Broad auto-triggering can invoke Douyin collection for ambiguous short-video research requests even when the user does not name Douyin.

Mitigation: Confirm the intended platform, target, and result limit before running collection commands in ambiguous workflows.

Risk: Runtime authentication messages may contradict the documented neutral-error requirement.

Mitigation: Review and patch runtime error handling before deployment so failed authentication does not disclose promotional or unnecessary support information.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-competitor-intel-source)
- [Usage Documentation](readme.md)
- [Complete Options Reference](references/options.md)
- [Changelog](references/changelog.md)
- [Input and Output JSON Schemas](assets/*.schema.json)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [JSON on stdout, operational logs on stderr, and saved JSON result files under logs/.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and sends API requests to www.guaikei.com; commands support configurable limits up to 10000 results.]

## Skill Version(s):

1.0.0 (source: package.json, references/changelog.md, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
