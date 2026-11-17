## Description:

Provides four command-line workflows for collecting public Douyin data: keyword and creator search, creator posts, video comments, and real-time hot trends, with structured JSON output and automatic logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, marketers, and content research teams use this skill to gather public Douyin videos, creator posts, comments, and hot-list data for content research, competitor analysis, sentiment review, and trend monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Douyin queries, URLs, and a GUAIKEI_API_TOKEN to the provider API.

Mitigation: Use a dedicated token with limited value, avoid submitting sensitive URLs or queries, and review token handling before installation.

Risk: The skill writes automatic JSON logs that may contain query terms, Douyin URLs, and collected public data.

Mitigation: Run it in a controlled workspace, restrict access to the logs directory, and remove logs that are no longer needed.

Risk: Generic short-video research prompts may activate the skill and collect external data when the user did not intend to query Douyin.

Mitigation: Constrain agent routing so the skill runs only for explicit Douyin public-data collection tasks.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-data-intake-to-json)
- [README](readme.md)
- [Command options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Search request schema](assets/search_cli_req.schema.json)
- [Search response schema](assets/search_cli_resp.schema.json)
- [Post request schema](assets/post_cli_req.schema.json)
- [Post response schema](assets/post_cli_resp.schema.json)
- [Comment request schema](assets/comment_cli_req.schema.json)
- [Comment response schema](assets/comment_cli_resp.schema.json)
- [Hot trends response schema](assets/hot_cli_resp.schema.json)
- [Token and support site](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Files, Shell commands, Guidance]

**Output Format:** [JSON on stdout with stderr logs and timestamped JSON files in logs/]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; commands return structured status, request metadata, and result objects.]

## Skill Version(s):

1.0.0 (source: package.json, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
