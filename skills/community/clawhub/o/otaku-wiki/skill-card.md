## Description:

Otaku Wiki helps agents answer anime, character, and voice actor questions by querying the AniList API and formatting Chinese encyclopedia-style responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robin797860](https://clawhub.ai/user/robin797860)

### License/Terms of Use:


## Use Case:

External users and anime community assistants use this skill to look up anime, character, and staff information from AniList and present concise Chinese knowledge-card answers with source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted user search terms may run unintended shell commands if interpolated into command strings.

Mitigation: Pass user search terms as separate arguments or apply robust shell quoting before invoking the AniList CLI.

Risk: The skill performs live network lookups.

Mitigation: Run in a constrained environment and limit outbound network access to AniList where possible.

## Reference(s):

- [AniList GraphQL API endpoint](https://graphql.anilist.co)
- [ClawHub skill page](https://clawhub.ai/robin797860/skills/otaku-wiki)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown response with AniList links and JSON CLI results used as intermediate evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and network access to AniList; no API key was detected.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
