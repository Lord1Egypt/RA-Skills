## Description:

Constructs GitHub Trending repository and developer links with optional filters for programming language, time range, and spoken or documentation language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[langlyyy](https://clawhub.ai/user/langlyyy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate direct GitHub Trending web links for repository or developer discovery, filtered by language, time window, or documentation language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may assume the generated links come from an official GitHub Trending API or live API query.

Mitigation: State that the skill constructs GitHub web URLs and that users should open GitHub to view current results.

Risk: Trending filter values may stop matching user intent if GitHub changes supported language labels or URL parameters.

Mitigation: Confirm language and spoken-language values on GitHub Trending when results do not match expectations.

## Reference(s):

- [GitHub Trending](https://github.com/trending)
- [GitHub Trending Developers](https://github.com/trending/developers)
- [GitHub Trending Language Parameters](references/languages.md)
- [GitHub Trending Spoken Language Parameters](references/spoken-languages.md)
- [ClawHub Skill Page](https://clawhub.ai/langlyyy/skills/github-trending-project)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with GitHub Trending URLs and brief filter explanations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces web links only; does not call the GitHub API or execute local code.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
