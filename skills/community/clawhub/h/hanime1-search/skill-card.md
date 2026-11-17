## Description:

当作者提及hanime是否更新时，或者miuuuu是否更新时，h站是否更新，调用此技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chgy123](https://clawhub.ai/user/chgy123)

### License/Terms of Use:

MIT-0

## Use Case:

External users or agents use this skill to check current search-result titles for a specific Hanime query when asked whether the referenced content has updated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes a request to hanime1.me, which can reveal interest in the configured search query.

Mitigation: Run it only when the user asks for this check and is comfortable with that network request.

Risk: The output is a current list of search-result titles, not a reliable historical update detector.

Mitigation: Treat the result as current page contents and verify updates against another source before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chgy123/skills/hanime1-search)
- [Hanime1 search page used by the skill](https://hanime1.me/search?query=miuuuuu)

## Skill Output:

**Output Type(s):** [Text, Shell commands]

**Output Format:** [Plain text terminal output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lists up to 10 current search-result titles from a fixed query.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
