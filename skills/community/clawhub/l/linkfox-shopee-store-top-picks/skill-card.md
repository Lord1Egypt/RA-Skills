## Description:

Shopee Top Picks helps agents manage selected product collections for authorized Shopee stores through LinkFox, covering list, create, update, and delete operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce operators, and their agents use this skill to inspect and manage Shopee Top Picks collections for an authorized store through LinkFox. It supports listing, creating, updating, and deleting Top Picks collections while preserving JSON responses for later review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires LinkFox credentials and can access live Shopee store operations.

Mitigation: Install and run it only in environments where LinkFox credentials are approved, and treat generated API keys as secrets.

Risk: Create, update, and delete operations can mutate Shopee Top Picks collections.

Mitigation: Confirm each create, update, or delete action manually before running the command against an authorized store.

Risk: Endpoint override environment variables can redirect requests.

Mitigation: Avoid endpoint overrides unless the target service is trusted and expected for the task.

Risk: Saved LinkFox response files may contain store or account data.

Mitigation: Review retention expectations and periodically delete saved response files that are no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-shopee-store-top-picks)
- [Shopee Top Picks API Index](https://open.shopee.com/documents/v2/v2.top_picks.get_top_picks_list?module=100&type=1)
- [Top Picks API Reference](references/api.md)
- [Add Top Picks](references/apis/add-top-picks.md)
- [Delete Top Picks](references/apis/delete-top-picks.md)
- [Get Top Picks List](references/apis/get-top-picks-list.md)
- [Update Top Picks](references/apis/update-top-picks.md)
- [LinkFox Auth and Billing Onboarding](references/onboarding.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, JSON files]

**Output Format:** [Markdown guidance with shell commands and JSON API responses saved to local files or printed to stdout.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full responses are saved under linkfox/<date>/<session>/data; large responses print a summary unless --inline is used.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
