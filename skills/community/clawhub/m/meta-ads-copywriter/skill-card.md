## Description:

Meta Ads Copywriter helps agents generate direct-response copy variations, UTM-tagged campaign URLs, and visual creative publishing actions for Meta Ads through the Habilis MCP Gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafacpti23](https://clawhub.ai/user/rafacpti23)

### License/Terms of Use:

MIT-0

## Use Case:

External advertisers, marketing operators, and developers use this skill to draft Meta Ads copy variants, prepare tracked campaign URLs, and route approved creative publishing actions through a configured Habilis MCP Gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can let an agent work with live Meta Ads assets through a third-party gateway.

Mitigation: Use least-privilege, account-limited, short-lived credentials and manually confirm each upload, creative creation, or ad update.

Risk: Gateway logging, retention, token handling, and spend controls are not fully specified in the evidence.

Mitigation: Clarify gateway data handling and spend safeguards before using production ad accounts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rafacpti23/skills/meta-ads-copywriter)
- [Habilis MCP Gateway](https://xvix.com.br)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown with inline bash and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke Meta Ads upload, creative creation, and ad update tools when the required Habilis and Meta Ads credentials are configured.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter and clawhub.json report 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
