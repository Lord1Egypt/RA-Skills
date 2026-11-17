## Description:

Uses an OOMOL-connected DeepSeek account to create model responses, search or fetch web pages, list models, and check account balance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People with a connected DeepSeek account can use this skill to generate responses, search and fetch web content, inspect available models, and check account balance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs downloaded installers that have not been verified, and the CLI can make persistent changes to agent skills.

Mitigation: Review and verify the specific CLI release before installation; set OO_SKILLS_SYNC_DISABLED=1 before invoking it to disable automatic agent-skill changes.

Risk: Requests may use shared prompt content and account spending.

Mitigation: Limit shared prompts and spending to your intended request.

## Reference(s):

- [DeepSeek API documentation](https://api-docs.deepseek.com/)
- [DeepSeek platform](https://platform.deepseek.com)
- [oo CLI repository (tool reference)](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Text or JSON responses, including Markdown page content where requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The response format and content depend on the selected action.]

## Skill Version(s):

1.0.7 (source: SKILL.md frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
