## Description:

Use the RiteKit connector to retrieve hashtag statistics and trends, clean hashtags, and generate hashtag suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to query RiteKit hashtag data and request hashtag recommendations for text, URLs, or images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI dependency can install or update other agent skills without clearly disclosing the full scope of those changes.

Mitigation: Review and install the CLI separately, and decide whether OO_SKILLS_SYNC_DISABLED is appropriate before enabling the skill.

Risk: The hosted connector and remote installer were not fully verified; OOMOL mediates RiteKit requests and credentials.

Mitigation: Review the connector setup and avoid routing information or credentials through OOMOL unless that handling is acceptable.

## Reference(s):

- [RiteKit](https://ritekit.com/)
- [RiteKit API documentation](https://documenter.getpostman.com/view/2010712/SzS7Qku5?version=latest)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Text summaries and structured JSON connector results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs follow the live connector schema.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
