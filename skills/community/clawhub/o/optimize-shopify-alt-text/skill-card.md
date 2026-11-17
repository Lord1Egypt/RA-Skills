## Description:

Audit and safely improve Shopify image alt text for product media, collection images, article featured images, and article inline images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvsao](https://clawhub.ai/user/lvsao)

### License/Terms of Use:

MIT-0

## Use Case:

Shopify merchants, ecommerce operators, and supporting agents use this skill to audit image alt text, prepare visually grounded optimization plans, and apply approved alt text updates across product, collection, and article images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict flags review-before-install concerns because the skill can update itself.

Mitigation: Use a pinned, reviewed release and review any available update before installing or running it.

Risk: The skill needs Shopify read and write permissions for products, content, and files to complete approved updates.

Mitigation: Prefer the quick Shopify CLI connection, grant only the scopes needed for the active task, and require preview plus explicit approval before execution.

Risk: Private Shopify store configuration and Dev Dashboard credentials may be present in runtime environment files.

Mitigation: Keep skill-hub.env and Dev Dashboard credentials private, ignored by source control, and outside the installed skill directory.

Risk: Generated alt text can be inaccurate if based on metadata alone instead of image content.

Mitigation: Require a working vision model and at least three pixel-derived facts before proposing any alt text candidate.

## Reference(s):

- [Shopify Alt Text Rules](artifact/references/alt-text-rules.md)
- [Connect Your Store](artifact/references/onboarding-guide.md)
- [Project homepage](https://github.com/lvsao/shopify-skill-hub)
- [ClawHub skill page](https://clawhub.ai/lvsao/skills/optimize-shopify-alt-text)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Conversational Markdown with command examples, helper stdout, and JSON preview or execution results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires verified image evidence for alt text candidates and explicit approval before Shopify writes.]

## Skill Version(s):

2.2.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
