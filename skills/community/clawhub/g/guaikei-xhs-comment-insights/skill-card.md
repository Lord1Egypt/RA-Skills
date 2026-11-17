## Description:

Collects public Xiaohongshu posts, post details, creator works, and comments so an agent can support content, competitor, KOL, comment, and trend analysis without using a logged-in Xiaohongshu account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, content creators, data analysts, and agents use this skill to retrieve public Xiaohongshu search results, note details, creator posts, and comments for reporting, competitor monitoring, sentiment review, and trend research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends GUAIKEI_API_TOKEN, Xiaohongshu URLs, keywords, and requested collection limits to guaikei.com.

Mitigation: Confirm that this external data transfer is approved for the intended use, scope the token to the minimum needed access, and rotate it if exposure is suspected.

Risk: The implementation places GUAIKEI_API_TOKEN in request URLs.

Mitigation: Treat the token as sensitive, avoid sharing command output or network traces that may contain URLs, and prefer controlled execution environments.

Risk: Fetched post and comment results are saved locally under logs/.

Mitigation: Apply the user's data retention and access-control policy to generated log files and remove them when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-comment-insights)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Guaikei service site](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Analysis, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; command results are structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; fetched post and comment results may be saved locally under logs/.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
