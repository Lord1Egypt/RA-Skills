## Description:

Jike Data Service helps agents query Douyin content-marketing data for Honor-focused competitor account discovery, keyword and trend analysis, topic suggestions, and benchmark content search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzoob](https://clawhub.ai/user/mzoob)

### License/Terms of Use:

MIT-0

## Use Case:

Content marketers and content architects use this skill to find Honor and competitor Douyin accounts, videos, keyword rankings, hot videos, hashtags, and topic candidates for campaign analysis and content planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed through local configuration or command output.

Mitigation: Prefer RY_DATA_SECRET_KEY over scripts/config.json, keep transcripts and logs private, and avoid running the check command where masked key fragments may be disclosed.

Risk: Changing the API base URL can route authenticated requests to an untrusted service.

Mitigation: Use the default service or another trusted HTTPS origin only, and review any RY_DATA_BASE_URL or config.json base_url change before execution.

Risk: Keyword add and delete commands can change remote keyword monitoring state.

Mitigation: Require explicit user approval and confirm the exact keyword before running keywords add or keywords delete.

## Reference(s):

- [Workflow Guide](references/workflow-guide.md)
- [CLI Reference](references/cli-reference.md)
- [Jike Data Service API](https://ry-api.dso100.com)
- [ClawHub Skill Page](https://clawhub.ai/mzoob/skills/jike-data-service)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell commands; CLI responses are formatted text by default and JSON when --json is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and an API key supplied through RY_DATA_SECRET_KEY or scripts/config.json; list commands support pagination.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
