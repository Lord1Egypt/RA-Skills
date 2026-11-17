## Description:

Get a daily digest of trending posts from Moltbook with Chinese summaries. Uses Google Translate for full Chinese translation of post content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangfugui1799](https://clawhub.ai/user/wangfugui1799)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to fetch Moltbook posts and produce a concise daily digest with Chinese summaries, ranking metadata, and links to the original posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to a Moltbook API key.

Mitigation: Use a dedicated, least-privilege Moltbook token and avoid running the skill with elevated privileges.

Risk: Summary text may be sent to Google Translate through deep-translator.

Mitigation: Use the skill only when that data flow is acceptable for the posts being summarized.

Risk: Generated Chinese summaries may omit nuance from the original posts.

Mitigation: Use the linked Moltbook posts as the source of truth when accuracy matters.

## Reference(s):

- [Moltbook API Reference](references/api.md)
- [Moltbook API Base URL](https://www.moltbook.com/api/v1)
- [Moltbook Explore](https://moltbook.com/explore)
- [ClawHub Skill Page](https://clawhub.ai/wangfugui1799/skills/moltbook-daily-digest)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, configuration]

**Output Format:** [Markdown daily digest with Chinese summaries, post rankings, engagement counts, and source links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Moltbook API key and may send summary text to Google Translate through deep-translator.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
