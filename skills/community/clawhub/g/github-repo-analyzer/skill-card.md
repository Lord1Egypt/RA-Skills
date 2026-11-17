## Description:

Analyze GitHub repositories to provide statistics, contributor activity, programming languages, and issue and PR trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dagangtj](https://clawhub.ai/user/dagangtj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect public GitHub repositories for repository statistics, contributor activity, language usage, and project metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository names or URLs analyzed with the skill are sent to GitHub's API.

Mitigation: Avoid submitting private or sensitive repository identifiers unless sending them to GitHub is acceptable.

Risk: The advertised issue and pull request trend features appear broader than the bundled script behavior.

Mitigation: Treat outputs as current public repository metadata and verify trend claims before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dagangtj/skills/github-repo-analyzer)
- [README.md](README.md)
- [SKILL.md](SKILL.md)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON repository analysis with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries GitHub's public API for repository metadata, languages, and top contributors.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
