## Description:

Queries Chinese couplets from Jike API by keyword or returns a random couplet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search for Chinese couplets by upper-line or lower-line keywords, or to retrieve a random couplet for writing, recommendation, or explanation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send the Jike API key and couplet keywords to an environment-selected API base URL if JIKE_API_BASE_URL is set.

Mitigation: Install only when use of a Jike API key is acceptable, and leave JIKE_API_BASE_URL unset unless the destination is trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/skills/jike-couplet-query)
- [Publisher profile](https://clawhub.ai/user/jikeapi-cn)
- [Jike API homepage](https://www.jikeapi.cn/)
- [Jike couplet query endpoint](https://api.jikeapi.cn/v1/couplet/query)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain-text table output or JSON from a Python CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Jike AppKey. Text table output truncates long fields; JSON output preserves the API payload.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
