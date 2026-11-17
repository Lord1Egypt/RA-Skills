## Description:

DataForB2B (dataforb2b.ai). Use this skill for ANY DataForB2B request — searching and reading data. Whenever a task involves DataForB2B, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to search DataForB2B people and companies, count results, retrieve account status, and enrich company or profile records through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup directs users to execute remote CLI installers without clear control over local changes.

Mitigation: Use a separately approved, version-pinned CLI installation with verified integrity, and review which agent skills it installs or updates.

Risk: DataForB2B requests use the connected account and may consume service credits.

Mitigation: Check the connected account balance and expected usage before running searches or enrichment actions.

## Reference(s):

- [DataForB2B](https://dataforb2b.ai)
- [DataForB2B API documentation](https://docs.dataforb2b.ai/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [DataForB2B ClawHub listing](https://clawhub.ai/oomol/skills/oo-dataforb2b)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON action responses with concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Response fields depend on the selected action and its live connector schema.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
