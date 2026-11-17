## Description:

Helps an agent manage LinkBunny backlink exchanges, including site setup, assignment review, and owner-approved placement reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkbunny](https://clawhub.ai/user/linkbunny)

### License/Terms of Use:

MIT-0

## Use Case:

Site owners and developers use this skill to set up a LinkBunny account and manage contextual backlink exchange assignments. It guides owner-approved site registration, placement review, reporting, and rejection while protecting credentials and site publishing decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing links and changing account or site settings can affect the owner’s sites and account; LinkBunny also receives registered site information and placement reports.

Mitigation: Require specific owner approval for consequential actions, review each proposed link before publication, and keep the API token in an owner-approved secret store outside Git.

Risk: Backlink results are self-reported, and the skill makes no promise of search-ranking benefit or search-policy safety.

Mitigation: Describe reports as recorded placements and avoid promising ranking, traffic, or search-policy outcomes.

## Reference(s):

- [LinkBunny agent documentation](https://getlinkbunny.com/docs/agents?ref=clawhub)
- [LinkBunny ClawHub listing](https://clawhub.ai/linkbunny/skills/linkbunny)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Shell commands, Configuration instructions]

**Output Format:** [Human-readable guidance with shell command examples and API request details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Consequential account, billing, site, assignment, and publishing actions require specific owner authorization.]

## Skill Version(s):

1.2.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
