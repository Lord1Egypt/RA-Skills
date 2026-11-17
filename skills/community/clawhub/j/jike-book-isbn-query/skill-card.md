## Description:

输入 ISBN-10 或 ISBN-13，查询书名、作者、译者、出版社、出版日期、页数、定价、装帧、丛书和封面等图书信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up publication metadata for ISBN-10 or ISBN-13 values through Jike's book ISBN query API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill honors an undocumented JIKE_API_BASE_URL override that could send the user's AppKey to an unintended server.

Mitigation: Run it only where JIKE_API_BASE_URL cannot be set by untrusted code, and leave that variable unset for normal use.

Risk: Passing the AppKey with --key may expose the credential through local command-line argument visibility.

Mitigation: Prefer JIKE_BOOK_ISBN_QUERY_KEY or JIKE_APPKEY environment variables for credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/skills/jike-book-isbn-query)
- [Jike API homepage](https://www.jikeapi.cn/)
- [ISBN query API endpoint](https://api.jikeapi.cn/v1/book/isbn/query)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON from a Python command-line script, summarized by the agent for the user]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an ISBN-10 or ISBN-13 and a Jike AppKey; API requests include the ISBN and AppKey.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
