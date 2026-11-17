## Description:

Automates job searches across Moroccan job boards with 7-day filtering, profile-based scoring, and a weekly Markdown report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elfilalihamza](https://clawhub.ai/user/elfilalihamza)

### License/Terms of Use:

MIT-0

## Use Case:

External users and job seekers use this skill to search Moroccan job boards, filter recent postings against a local profile, score matches, and produce a weekly application report.

### Deployment Geography for Use:

Morocco

## Known Risks and Mitigations:

Risk: The skill can fetch broadly configurable job-board URLs and may send profile-derived role, keyword, and location search terms to public job sites.

Mitigation: Use trusted public HTTPS job-board hosts, keep platform configuration limited to known sites, and avoid including sensitive personal details in the local profile.

Risk: Generated job reports may include stale, incorrect, or unverified job listing links.

Mitigation: Verify each listing on the original platform before applying and prefer directly extracted, tested URLs over constructed links.

## Reference(s):

- [Job Watch Skill Page](https://clawhub.ai/elfilalihamza/skills/job-watch)
- [Publisher Profile](https://clawhub.ai/user/elfilalihamza)
- [Initial Setup](references/initial-setup.md)
- [URL Extraction Guide](references/url-extraction-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown report saved locally and echoed in chat]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Filters postings from the last 7 days, scores matches from 0-100, and groups results by score band.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
