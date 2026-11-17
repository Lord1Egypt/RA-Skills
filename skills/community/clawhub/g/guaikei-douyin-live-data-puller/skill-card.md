## Description:

Guaikei Douyin Live Data Puller helps agents search public Douyin content, fetch creator posts and video comments, and retrieve real-time hot lists as structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and content analysts use this skill to collect public Douyin search results, creator posts, video comments, and hot-list data for content research, competitor analysis, public-opinion review, and trend monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Douyin search terms, target account or video URLs, limits, and GUAIKEI_API_TOKEN-dependent requests to the Guaikei service.

Mitigation: Use it only for intended public Douyin data collection, treat GUAIKEI_API_TOKEN as sensitive, and avoid sharing prompts or targets that should not leave the local environment.

Risk: Broad activation language can cause collection to run for short-video research prompts that do not explicitly mention Douyin.

Mitigation: Confirm the user intends Douyin collection before running commands when the platform is ambiguous.

Risk: Collected results are automatically retained in local JSON logs.

Mitigation: Review and remove files under logs/ after use when the collected data should not be retained.

Risk: Security evidence flags credential handling, promotional authentication errors, broad activation, and automatic local retention as review-worthy.

Mitigation: Prefer a release that narrows activation, keeps credentials out of URLs, removes runtime promotional contact messages, and makes result logging opt-in.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-live-data-puller)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Usage documentation](readme.md)
- [Options reference](references/options.md)
- [JSON schemas](assets/*.schema.json)
- [Changelog](references/changelog.md)
- [Guaikei service site](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Files, Guidance]

**Output Format:** [Structured JSON on stdout, diagnostic text on stderr, and timestamped JSON log files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14 or newer and a GUAIKEI_API_TOKEN; individual commands accept keywords, Douyin user or video URLs, limits, sorting, time range, duration, and content-type filters.]

## Skill Version(s):

1.0.0 (source: package.json, changelog, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
