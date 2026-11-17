## Description:

A Chinese-language dashboard for tracking UUMit digital assets, UT balances, ClawHub paid skills, and project or task progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cx75227-ops](https://clawhub.ai/user/cx75227-ops)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to view a browser-based information panel for UUMit asset status, UT balances, ClawHub paid skill listings, and task progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The page contacts the UUMit API from the browser to load live asset data.

Mitigation: Review and approve this external network access before installing or serving the site in a restricted environment.

Risk: The artifact names a specific ClawHub account.

Mitigation: Confirm the account context is appropriate for the intended user; the security evidence found no code that logs in, reads credentials, or changes account data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cx75227-ops/skills/moneytoolkit-site)
- [Publisher Profile](https://clawhub.ai/user/cx75227-ops)
- [UUMit Digital Assets API](https://api.uumit.com/api/v1/digital-assets)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with installation commands and browser dashboard behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The released site displays Chinese-language dashboard content and fetches live UUMit asset data from the browser.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
