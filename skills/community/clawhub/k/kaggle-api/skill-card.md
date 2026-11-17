## Description:

Helps agents search, download, and interact with Kaggle datasets, models, competitions, and notebooks through Maton-managed authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maton](https://clawhub.ai/user/maton)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other Kaggle users can use this skill to locate and retrieve datasets, models, competition information, and notebooks through an authorized Maton connection. Optional hosted functions and triggers support user-approved automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kaggle access is mediated by a Maton connection and its authentication permissions.

Mitigation: Confirm the user intends to connect Kaggle; prefer OAuth to a long-lived API key and use only the access required for the task.

Risk: Writes and hosted automation can modify resources or run under the connected account.

Mitigation: Default to reading and listing; obtain explicit approval for each write, new connection, and hosted function or trigger action.

Risk: Trigger destinations can forward matching event data continuously until removed.

Mitigation: Review and explicitly approve each destination and its recipient before enabling it; remove it when no longer needed.

## Reference(s):

- [Kaggle API documentation](https://www.kaggle.com/docs/api)
- [Maton](https://maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Kaggle skill on ClawHub](https://clawhub.ai/maton/skills/kaggle-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance]

**Output Format:** [Text or Markdown with CLI commands, API examples, and returned resource information]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the user's authorized Kaggle connection and available network access.]

## Skill Version(s):

1.2.5 (source: ClawHub release; skill frontmatter lists 1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
