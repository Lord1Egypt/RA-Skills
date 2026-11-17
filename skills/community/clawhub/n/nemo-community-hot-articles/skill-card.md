## Description:

Get trending articles from Nemo community/从Nemo社区获取热门文章 (no API key required).

This skill is ready for commercial/non-commercial use.

## Publisher:

[geeeeeeeeeeeeeeeek](https://clawhub.ai/user/geeeeeeeeeeeeeeeek)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch and inspect currently popular Nemo community articles through a public API call.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to link-nemo.com when used.

Mitigation: Review network access expectations before deployment and allow the request only in environments where this external public API is acceptable.

Risk: The documented example pipes API output through jq, which may not be installed in every runtime.

Mitigation: Install jq for the exact example command or adapt the response parsing to tools already available in the agent environment.

## Reference(s):

- [Nemo Popular Articles](https://www.link-nemo.com/popular)
- [Nemo Popular Articles API](https://www.link-nemo.com/api/popular/article)
- [ClawHub Skill Page](https://clawhub.ai/geeeeeeeeeeeeeeeek/skills/nemo-community-hot-articles)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls]

**Output Format:** [Markdown with inline bash code blocks and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses curl against the public link-nemo.com popular articles endpoint; no API key is requested.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
