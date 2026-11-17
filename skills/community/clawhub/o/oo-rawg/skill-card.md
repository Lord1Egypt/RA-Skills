## Description:

RAWG (rawg.io). Use this skill for ANY RAWG request — searching and reading data. Whenever a task involves RAWG, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can search RAWG and retrieve details about games, genres, platforms, developers, publishers, stores, tags, and related game media through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes unverified remote code and may introduce additional managed skills without a separate user choice.

Mitigation: Review and verify the oo CLI installation before setup, decide whether to permit additional managed skills, and set OO_SKILLS_SYNC_DISABLED=1 to prevent startup skill writes.

Risk: RAWG requests and account credentials are handled through OOMOL, and use may consume credits.

Mitigation: Confirm the RAWG connection and expected OOMOL credit usage before making requests.

## Reference(s):

- [RAWG](https://rawg.io)
- [RAWG API documentation](https://api.rawg.io/docs/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI command documentation](https://raw.githubusercontent.com/oomol-lab/oo-cli/main/docs/commands.md)
- [RAWG ClawHub release](https://clawhub.ai/oomol/skills/oo-rawg)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands, Configuration guidance]

**Output Format:** [JSON connector responses and text summaries; Markdown setup guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the selected RAWG action and its input schema.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
