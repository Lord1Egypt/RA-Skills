## Description:

Search and analyze TikTok KOLs using the KOLens API, including creator discovery, metrics, and optional contact fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maweis1981](https://clawhub.ai/user/maweis1981)

### License/Terms of Use:

MIT-0

## Use Case:

External users and growth teams use this skill to submit TikTok KOL search jobs, poll job status, query creator lists, and inspect follower, view, engagement, and contact data for legitimate outreach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Collecting creator contact data can create privacy, anti-spam, or outreach compliance obligations.

Mitigation: Use the skill only for legitimate outreach, avoid fetching contacts unless needed, and follow applicable privacy and anti-spam laws.

Risk: A misconfigured or untrusted KOLENS_API_URL could expose API keys or search activity.

Mitigation: Use only the verified HTTPS endpoint from the KOLens service administrator and keep API keys scoped and revocable.

Risk: Creator metrics and contact details returned by the API may be stale, incomplete, or unsuitable for immediate outreach.

Mitigation: Verify contact information and creator fit before taking action based on API results.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KOLENS_API_KEY, KOLENS_API_URL, curl, and optionally jq; API responses may include creator contact data when requested.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
