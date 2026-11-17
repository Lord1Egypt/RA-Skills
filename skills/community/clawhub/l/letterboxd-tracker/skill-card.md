## Description:

Your personal movie assistant. Track what you watch, check your lists, and get movie info from Letterboxd instantly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tamil-9421](https://clawhub.ai/user/tamil-9421)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to look up public Letterboxd profile statistics, diary entries, watchlists, and movie details from a supplied username or movie slug.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the unpinned third-party Python package `letterboxdpy`.

Mitigation: Install in a virtual environment and pin or review the package before deployment.

Risk: The skill fetches public Letterboxd data for supplied usernames and movie slugs.

Mitigation: Use only public identifiers that the user intends to query; do not treat the skill as a private account-data manager.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tamil-9421/skills/letterboxd-tracker)
- [Publisher Profile](https://clawhub.ai/user/tamil-9421)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON-formatted lookup results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public Letterboxd lookups; result size can be limited for diary and watchlist commands.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and README state 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
