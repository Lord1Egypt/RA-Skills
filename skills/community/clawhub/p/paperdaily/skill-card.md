## Description:

PaperDaily recommends high-value recent computer science papers from arXiv.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xyc5872](https://clawhub.ai/user/xyc5872)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams can use this skill to request daily or refreshed arXiv computer science paper recommendations, filtered by recency, keyword relevance, and information density.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Feishu application credentials and a chat ID.

Mitigation: Use a least-privilege Feishu app, limit workspace permissions, protect the App Secret, and rotate it if exposure is suspected.

Risk: Most runtime behavior is delegated to an unpinned external npm package that was not included for inspection.

Mitigation: Install only after reviewing the resolved openclaw-paperdaily package version, and prefer a release with a pinned dependency and lockfile.

## Reference(s):

- [Feishu Open Platform](https://open.feishu.cn/)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown or plain text paper recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations are triggered by the Chinese commands "今日文献" and "刷新文献".]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact package.json and skill.json list 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
