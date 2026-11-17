## Description:

MasterChef helps agents answer recipe and ingredient questions by querying api.yummy.chat for dish suggestions and recipes, translating between English and Chinese when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yummy-chat](https://clawhub.ai/user/yummy-chat)

### License/Terms of Use:

MIT-0

## Use Case:

External users ask an agent for recipe lookup or ingredient-based meal ideas, including English or Chinese requests. The skill guides the agent to query the Yummy recipe service, translate when needed, and return formatted cooking guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill pre-authorizes unrestricted Bash for API lookups.

Mitigation: Review Bash use before deployment and prefer a scoped HTTP/JSON mechanism or tightly limited commands for the required API calls.

Risk: Broad activation rules can trigger the skill on general cooking mentions.

Mitigation: Narrow activation to explicit recipe or ingredient-search requests and confirm ambiguous user intent before making API calls.

Risk: Recipe queries are sent to api.yummy.chat.

Mitigation: Avoid sending sensitive personal, dietary, or location information unless appropriate for the deployment context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yummy-chat/skills/masterchef)
- [ClawHub publisher profile](https://clawhub.ai/user/yummy-chat)
- [Yummy recipe API](https://api.yummy.chat)
- [Ingredient search endpoint](https://api.yummy.chat/ingredients)
- [Recipe lookup endpoint](https://api.yummy.chat/howtocook)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text recipe guidance, with shell commands used by the agent for API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May translate user inputs to Chinese before API calls and translate Chinese recipe responses back to the user's language.]

## Skill Version(s):

0.6.2 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
