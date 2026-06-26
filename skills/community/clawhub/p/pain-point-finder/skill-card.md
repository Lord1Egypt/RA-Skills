## Description: <br>
Discover pain points, frustrations, and unmet needs on Reddit using PullPush API, with no API keys required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanji84](https://clawhub.ai/user/yanji84) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, product teams, founders, and researchers use this skill to identify Reddit complaints, unmet needs, agreement signals, attempted solutions, and opportunity areas for product discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outputs may include third-party Reddit content, usernames, or sensitive details from public discussions. <br>
Mitigation: Prefer summaries over long quotes, avoid storing unnecessary personal details, and redact usernames or sensitive details before sharing results. <br>
Risk: Market opportunities inferred from Reddit complaints may be incomplete or misleading without additional validation. <br>
Mitigation: Use the validationStrength, agreement counts, comment volume, and source subreddit as preliminary signals, then confirm findings with independent customer research before acting on them. <br>
Risk: The skill depends on PullPush availability and may return partial data during service errors, blocking, or rate limits. <br>
Mitigation: Review stderr progress messages and JSON status fields, rerun narrower searches when needed, and treat partial results as incomplete evidence. <br>


## Reference(s): <br>
- [Pain Point Finder Skill Page](https://clawhub.ai/yanji84/pain-point-finder) <br>
- [Pain Point Finder Implementation Plan](docs/pain_point_discovery.md) <br>
- [Subreddit Seed Lists](references/SUBREDDITS.md) <br>
- [PullPush API](https://api.pullpush.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, analysis, guidance] <br>
**Output Format:** [JSON command output and Markdown synthesis guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI progress is written to stderr; scan and deep-dive results include scored posts, agreement signals, solution attempts, mentioned tools, and validation strength.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
