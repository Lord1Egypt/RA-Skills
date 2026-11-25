## Description:

Searches selected social platforms for accounts or creators matching a keyword and returns a comparison table with names, bios, follower counts, and post counts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and partnership teams can search a selected social platform for accounts in a category and review a one-page shortlist with names, bios, follower counts, and post counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords are sent to Okdata, so sensitive terms could be disclosed to the service.

Mitigation: Avoid including confidential or sensitive terms in search queries.

Risk: The security scan could not resolve some local path-like references, leaving those references unchecked.

Mitigation: Review the release's referenced paths before use.

## Reference(s):

- [Okdata creator search guide](https://okdata.online/skills/creators/?src=skill-okdata-creators)
- [Okdata creator search guide (Chinese)](https://okdata.online/zh/skills/creators/?src=skill-okdata-creators)
- [Okdata agent setup guide](https://okdata.online/agents.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown table followed by a concise recommendation, charge total, and source attribution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One page per selected platform; leave unavailable figures blank and report the actual charge and fetch time.]

## Skill Version(s):

0.2.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
