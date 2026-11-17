## Description:

用 ISBN 查图书详情，或按书名关键字搜书。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up book details from an ISBN or search for books by title keyword, then summarize fields such as title, author, publisher, publication date, price, and description.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ISBNs, book search terms, and JISU_API_KEY are sent to JisuAPI.

Mitigation: Install only if that data sharing is acceptable, keep the API key scoped to this use, and avoid sensitive search terms.

Risk: Returned cover images and seller links are external content.

Mitigation: Treat returned links as external before automatically opening, rendering, or presenting them to users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/isbn)
- [JisuAPI ISBN documentation](https://www.jisuapi.com/api/isbn/)
- [JisuAPI homepage](https://www.jisuapi.com/)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON request or response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; API responses are returned as JSON from JisuAPI.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
