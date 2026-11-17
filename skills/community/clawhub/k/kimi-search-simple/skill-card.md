## Description:

通过 Kimi API 的 builtin_function $web_search 联网检索，用于新闻、实时信息、股价、公司动态等时效性内容，并支持中英检索和总结或原始结果两种输出模式。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhc888007](https://clawhub.ai/user/jhc888007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to retrieve current web information through Moonshot/Kimi search and return either a concise synthesized answer or source-oriented result entries for time-sensitive questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Moonshot's API.

Mitigation: Use the skill only when sending the query content to Moonshot is acceptable.

Risk: The skill requires a Moonshot/Kimi API key from environment variables or documented local credential files.

Mitigation: Store the API key in an environment variable or protected credential file, and avoid embedding secrets in prompts or source files.

Risk: Dependency versions are not pinned in the artifact instructions.

Mitigation: Use a virtual environment and pinned dependency versions for reproducible installs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jhc888007/skills/kimi-search-simple)
- [Moonshot platform](https://platform.moonshot.cn/)
- [Moonshot API endpoint](https://api.moonshot.cn/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown or plain text responses, with shell commands and Python snippets for invocation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default mode returns a synthesized answer; raw mode returns source-oriented Title, Date, URL, and Summary entries.]

## Skill Version(s):

1.0.10 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
