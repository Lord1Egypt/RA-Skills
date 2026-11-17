## Description:

This skill helps agents search Douyin, collect public creator posts and video comments, and retrieve real-time trending lists as structured JSON for content research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, marketers, and content analysts use this skill to gather public Douyin search results, creator posts, comments, and trend data for short-video research, competitor analysis, sentiment review, and hotspot tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends keywords, Douyin URLs, and a private Guaikei API token to the Guaikei service, with the token included in URL parameters.

Mitigation: Use a low-privilege, revocable token; rotate it periodically; avoid submitting sensitive research terms or private URLs.

Risk: The skill automatically writes collected research data to local log files.

Mitigation: Store logs in a protected workspace, review them before sharing, and delete them when they are no longer needed.

Risk: The activation rules are broad enough that ambiguous short-video research prompts may trigger the skill even when Douyin is not explicitly requested.

Mitigation: Confirm that the user wants Douyin public-data collection before running commands for ambiguous prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-hotspot-radar)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Usage documentation](artifact/readme.md)
- [CLI options reference](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)
- [CLI input and output schemas](artifact/assets/)
- [Guaikei service documentation](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [JSON on stdout, logs on stderr, and saved JSON log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=16.14 and a GUAIKEI_API_TOKEN environment variable; CLI commands must run from the skill root.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, changelog, constants.js)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
