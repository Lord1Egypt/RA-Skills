## Description:

Full Goodreads integration: read shelves, search books, get details and reviews via RSS, and perform write actions such as rating, shelving, reviewing, editing dates, and updating progress through Playwright browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phuc-nt](https://clawhub.ai/user/phuc-nt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to inspect Goodreads shelves, activity, book details, and reviews, then update authenticated Goodreads account data such as ratings, shelves, reviews, reading dates, and progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a reusable authenticated Goodreads browser session.

Mitigation: Use a dedicated virtual environment and OS user where practical, protect scripts/.browser-data, and periodically delete the stored browser data when access is no longer needed.

Risk: Write actions can change Goodreads ratings, shelves, reviews, reading dates, and progress.

Mitigation: Review every proposed write command and its target book before execution, especially for account-changing actions.

Risk: Stealth browser automation and weakened browser isolation increase operational and account-safety risk.

Mitigation: Install only when this risk is acceptable, consider removing stealth or no-sandbox behavior, and pin dependencies before use.

## Reference(s):

- [Goodreads Skill setup guide](references/SETUP.md)
- [ClawHub skill release](https://clawhub.ai/phuc-nt/skills/goodreads-full)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read commands return Goodreads data as JSON; write commands return JSON status and may modify the authenticated Goodreads account.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
