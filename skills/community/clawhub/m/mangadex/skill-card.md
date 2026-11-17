## Description:

MangaDex CLI skill for search, manga/chapter lookup, follow-feed checks, and recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtsku](https://clawhub.ai/user/mtsku)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to search MangaDex, inspect manga and chapter metadata, check authenticated follow-feed updates, and request recommendation-oriented CLI queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install an unpinned global npm package, which can introduce unreviewed third-party code into the runtime.

Mitigation: Review the npm package source before installation and pin or isolate the package version where possible.

Risk: The authentication workflow includes command-line handling of MangaDex client secrets, passwords, and access tokens.

Mitigation: Prefer unauthenticated public lookups unless account-specific features are required, and avoid entering secrets into command lines or agent-visible transcripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mtsku/skills/mangadex)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text, JSON]

**Output Format:** [Markdown guidance with CLI command examples and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public read endpoints can run without authentication; feed updates and library-aware recommendations require MangaDex authentication.]

## Skill Version(s):

0.1.2 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
