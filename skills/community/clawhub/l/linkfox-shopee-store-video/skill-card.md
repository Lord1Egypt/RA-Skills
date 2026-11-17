## Description:

Helps agents manage and analyze Shopee store videos through LinkFox scripts covering the Shopee Open API Video module.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and ecommerce operators use this skill to publish, edit, delete, list, and analyze Shopee store videos for authorized shops through agent-driven scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is suspicious because the skill can handle LinkFox account setup, phone/SMS authentication, API keys, Shopee shop and video data, billing order creation, automatic feedback calls, and local response files.

Mitigation: Install only after reviewing the workflow, use trusted LinkFox HTTPS endpoints, avoid sharing SMS codes unless the workflow is trusted, and clean up saved response files and shell-profile API keys when no longer needed.

Risk: The skill can perform state-changing Shopee video actions such as posting, editing, deleting, and billing-related order creation.

Mitigation: Review delete, edit, post, and order actions before execution, especially when they affect authorized shops or paid account operations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-shopee-store-video)
- [Shopee Open Platform Video Module](https://open.shopee.com/documents/v2/v2.video.get_cover_list?module=129&type=1)
- [API and Field Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses or saved JSON response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses are persisted under a local linkfox session data directory; large responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
