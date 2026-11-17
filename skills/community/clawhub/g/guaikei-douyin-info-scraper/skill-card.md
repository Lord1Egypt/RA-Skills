## Description:

This skill helps agents collect structured JSON from public Douyin keyword search, creator post, video comment, and trending-topic workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect public Douyin search results, creator posts, video comments, and trend lists for content research, competitor monitoring, sentiment analysis, and trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a Guaikei API token.

Mitigation: Use a dedicated, revocable token supplied through the environment, review the skill before installing, and avoid running it on shared machines for sensitive research.

Risk: The skill can collect and save scraped Douyin comments, profiles, creator posts, and trend data.

Mitigation: Confirm lawful basis and provider permission before collecting or redistributing data, and monitor or delete generated logs and outputs when they are no longer needed.

Risk: Broad trigger rules may run collection workflows in contexts where users do not expect saved scraped data.

Mitigation: Confirm the intended Douyin collection target and scope before execution, especially for multi-step research workflows.

## Reference(s):

- [Skill README](readme.md)
- [Complete option reference](references/options.md)
- [Changelog](references/changelog.md)
- [Search request schema](assets/search_cli_req.schema.json)
- [Search response schema](assets/search_cli_resp.schema.json)
- [Post request schema](assets/post_cli_req.schema.json)
- [Post response schema](assets/post_cli_resp.schema.json)
- [Comment request schema](assets/comment_cli_req.schema.json)
- [Comment response schema](assets/comment_cli_resp.schema.json)
- [Hot list response schema](assets/hot_cli_resp.schema.json)
- [Guaikei token and help site](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands; command stdout is JSON and logs may be saved as JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=16.14 and a GUAIKEI_API_TOKEN environment variable.]

## Skill Version(s):

1.0.0 (source: package.json, references/changelog.md, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
