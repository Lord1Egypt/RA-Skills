## Description:

博客监控技能 - 监控博客和网站更新，通过RSS或网页变化检测。

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content monitoring users can use this skill to assemble an RSS or webpage watcher that checks configured public blog URLs and reports detected updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches arbitrary user-provided URLs without documented network safety limits.

Mitigation: Restrict monitored URLs to public blog or RSS endpoints, avoid localhost, private-network, cloud metadata, and other sensitive URLs, and add URL validation before use.

Risk: Network requests may run without documented timeouts or response-size limits.

Mitigation: Use request timeouts, response-size limits, exception handling, and pinned dependency versions before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
