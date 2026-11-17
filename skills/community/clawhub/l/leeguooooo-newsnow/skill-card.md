## Description:

newsnow helps an agent fetch trending news and hot topics from 66 sources across 44 platforms, with structured items that can include titles, URLs, publication dates, and metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leeguooooo](https://clawhub.ai/user/leeguooooo)

### License/Terms of Use:


## Use Case:

External users and developers use newsnow to list supported sources, fetch trending topics from social, technology, finance, and news platforms, and request JSON output for downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running an unpinned npm package at runtime can execute package code that has not been reviewed for the deployed environment.

Mitigation: Review or pin the newsnow package before use and prefer a locally installed locked version over npx.

Risk: PRODUCTHUNT_API_TOKEN is required for the Product Hunt source and could be exposed more broadly than needed.

Mitigation: Provide PRODUCTHUNT_API_TOKEN only for the specific Product Hunt command in a minimal environment.

Risk: Some sources may be inaccessible or return blocked responses, including linuxdo endpoints that may return 403 Forbidden.

Mitigation: Treat source availability as best effort and choose alternate sources when a platform is blocked.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leeguooooo/skills/leeguooooo-newsnow)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require npm installation and PRODUCTHUNT_API_TOKEN for Product Hunt; some sources can fail due to access restrictions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
