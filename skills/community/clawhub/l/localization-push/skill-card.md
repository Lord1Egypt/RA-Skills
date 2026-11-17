## Description:

Localizes the user's own App Store / Google Play listing into new languages through their connected App Store Connect or Play Console account - picks target locales from markets with demand, researches the keywords people actually search in each country with AppGoat, writes a localized name, subtitle, keyword field and promotional text (Play title, short and full description) within the store limits, and pushes each locale as a dry run with a before/after diff the user approves.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafalzawadzki](https://clawhub.ai/user/rafalzawadzki)

### License/Terms of Use:

MIT-0

## Use Case:

App owners and ASO practitioners use this skill to research local search demand and prepare localized listing metadata for up to five App Store or Google Play locales. It normally presents dry-run diffs for review; the optional unattended workflow can apply proposals before human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional unattended workflow can apply store-listing changes before a person reviews them.

Mitigation: Use the interactive workflow and approve each diff. For unattended runs, enforce mandatory human approval in AppGoat or stop after proposals; pin downloaded playbooks to a reviewed commit.

## Reference(s):

- [AppGoat REST API Fallback](reference/api.md)
- [AppGoat Skills Repository (optional workflow dependency)](https://github.com/appgoat/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Localized store listing fields and Markdown diff tables with target keywords]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Up to five locales per run; store-specific metadata limits apply.]

## Skill Version(s):

1.0.0 (source: server-resolved release version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
