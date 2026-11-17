## Description:

Provides aggregated summaries and updates of public short videos, short dramas, and trending lists from Haokan video pages based on keywords or topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codenova58](https://clawhub.ai/user/codenova58)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to organize lightweight summaries of public Haokan short-video, short-drama, and ranking pages for internal analysis and alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill could be used on private, login-only, or restricted content.

Mitigation: Limit use to public Haokan pages and avoid collecting private or access-controlled data.

Risk: Automated collection could exceed platform expectations or trigger anti-abuse controls.

Mitigation: Keep request frequency low, avoid batch scraping, and follow the skill guidance against downloads, API calls, and bulk collection.

Risk: Summaries of public video metrics or rankings may be incomplete or stale.

Mitigation: Treat outputs as lightweight analysis aids and verify important conclusions against the source page.

## Reference(s):

- [Haokan Video](https://haokan.baidu.com/)
- [ClawHub skill page](https://clawhub.ai/codenova58/skills/haokan)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summaries and structured guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be based on public page information and avoid downloads, API calls, login-only data, or bulk collection.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
