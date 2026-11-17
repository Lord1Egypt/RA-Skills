## Description:

Uses Amazon's storefront Alexa shopping assistant to answer a single natural-language shopping prompt, return a guide-style answer, grouped product recommendations with ASINs, and follow-up questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill for conversational Amazon product discovery when a user wants Alexa-style shopping recommendations, product ASINs, prices, ratings, and suggested follow-up questions. It is best suited to one prompt at a time, with the agent summarizing prior answers before making any follow-up request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shopping prompts and page context are sent to LinkFox and may include user preferences or commercial research intent.

Mitigation: Use the skill only when the user accepts LinkFox processing those prompts, and avoid including sensitive personal or business information in shopping questions.

Risk: The skill can guide LinkFox account setup, SMS-code login, API-key provisioning, package purchase, and payment-order creation.

Mitigation: Ask the user before account or billing actions, share SMS codes only when the user intends to log in or register, and confirm plan and payment method before creating an order.

Risk: API keys or account details may appear in terminal output, logs, transcripts, or local files.

Mitigation: Treat keys as secrets, rotate any key that is exposed, and review local LinkFox output folders for retained prompts, responses, QR images, and credentials.

Risk: Environment endpoint overrides can redirect requests away from the default LinkFox services.

Mitigation: Use endpoint override environment variables only in trusted environments and remove unexpected overrides before handling real user data.

Risk: Repeated calls consume LinkFox credits and Alexa responses can vary between calls.

Mitigation: Use the script cache where appropriate, avoid automatic retry loops for empty or failed results, and explain additional cost before making follow-up calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-amazon-alexa-search)
- [Amazon Alexa shopping assistant API reference](references/api.md)
- [Authentication and billing onboarding](references/onboarding.md)
- [LinkFox Skills](https://skill.linkfox.com/)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown report or structured JSON, with full responses saved as local JSON files by the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each API call accepts one prompt; optional URL context can anchor the answer to a specific Amazon page.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
