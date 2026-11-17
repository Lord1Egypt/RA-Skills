## Description:

Checks approximate Google-indexed page counts for one or more domains using Google's site: search operator through Chrome Remote Debugging Protocol on localhost:9222.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgx-00](https://clawhub.ai/user/lgx-00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site operators, and SEO practitioners use this skill to estimate how many pages Google has indexed for a domain and to compare index coverage across multiple domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls Chrome through a remote debugging session that may share cookies, logins, and tabs from the active Chrome profile.

Mitigation: Run it only with a dedicated temporary Chrome profile, avoid unrelated logged-in accounts, close unrelated tabs before use, and verify the created tab is closed afterward.

Risk: The workflow may install the ws npm package at runtime without a pinned version.

Mitigation: Use a pinned or preinstalled ws dependency from a trusted package source before running the skill.

Risk: Google site: result counts are approximate and can vary across data centers.

Mitigation: Present results as estimates and use Google Search Console when precise indexing data is required.

## Reference(s):

- [Google Index Checker ClawHub Skill Page](https://clawhub.ai/lgx-00/skills/google-index-checker)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports approximate index counts and comparison tables; values can vary by Google data center and should not be treated as exact measurements.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
