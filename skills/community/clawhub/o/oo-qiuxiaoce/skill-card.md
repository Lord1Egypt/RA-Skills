## Description:

Search and read QiuXiaoCe football data through the connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can ask an agent to find fixtures, league and team information, standings, and match statistics from QiuXiaoCe.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback setup installs downloaded CLI code that was not verified and may synchronize agent skills automatically.

Mitigation: Review and explicitly approve the installer, use a verified fixed release, and check whether automatic skill synchronization is acceptable before running it.

Risk: Connecting QiuXiaoCe routes requests through OOMOL and may consume service credits.

Mitigation: Review the connection and available credits before querying.

## Reference(s):

- [QiuXiaoCe Data Documentation](https://www.qiuxiaoce.com/data-docs/)
- [QiuXiaoCe Homepage](https://www.qiuxiaoce.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown instructions and text or JSON data returned by QiuXiaoCe actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected action and available QiuXiaoCe data; queries may consume service credits.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
