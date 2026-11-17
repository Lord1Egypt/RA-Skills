## Description:

Researches Walmart US keywords with Sorftime, including hot keyword filters, reverse lookup from product names, product search results, keyword details, product-associated keywords, related keywords, and saved-keyword folder management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce operators, marketplace analysts, and developers use this skill to research Walmart US search demand, inspect keyword and product associations, expand related terms, and manage Sorftime saved-keyword folders through LinkFox.

### Deployment Geography for Use:

Global; the research data scope is Walmart US.

## Known Risks and Mitigations:

Risk: The skill sends API keys and business query details to LinkFox/Sorftime endpoints, and the gateway endpoint can be configured by environment variable.

Mitigation: Keep gateway and login endpoint overrides unset unless the operator trusts them, and share only the query details needed for the requested Walmart keyword task.

Risk: Saved-keyword operations can add, move, or delete external account data.

Mitigation: Require explicit confirmation before favoriteAdd or favoriteChange, confirm broad delete scope when no folder is supplied, and review returned business result codes.

Risk: Keyword research, pagination, expansion, onboarding, and order actions may consume paid credits or initiate billing flows.

Mitigation: Explain expected credit use before high-cost calls, repeated pages, related-keyword expansion, or purchases, and obtain user approval before billing actions.

Risk: Full API responses are written to local JSON files and may contain business-sensitive keyword, product, account, or billing context.

Mitigation: Store outputs only in the intended workspace, avoid unnecessary inline dumps, and handle generated JSON files as sensitive project data.

Risk: Feedback reporting can send intent and result context to LinkFox when behavior or results mismatch intent or feedback is detected.

Mitigation: Disable or decline feedback reporting unless the user intends to send that context to LinkFox.

## Reference(s):

- [Walmart keyword research API reference](artifact/references/api.md)
- [Authentication and billing onboarding guide](artifact/references/onboarding.md)
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-sorftime-walmart-keyword-research)
- [Publisher profile](https://clawhub.ai/user/linkfox-ai)
- [LinkFox skills site](https://skill.linkfox.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON files, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses; full responses are saved as JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses over 8 KB print a summary unless inline output is requested; read operations may use a 24-hour local cache, while saved-keyword operations bypass the cache.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
