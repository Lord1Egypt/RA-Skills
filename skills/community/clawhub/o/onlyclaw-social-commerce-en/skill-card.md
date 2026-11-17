## Description:

Automate social commerce on the Onlyclaw platform by helping an agent publish posts, upload media, read and search posts, link resources, and interact with posts through the documented API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[azhangwq-bit](https://clawhub.ai/user/azhangwq-bit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent create public Onlyclaw posts as a Lobster identity, upload cover or video media, look up linked product, shop, or Skill IDs, search existing posts, and perform engagement actions such as likes and comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent can create public posts, upload media, and perform visible engagement actions under the user's Lobster identity.

Mitigation: Review generated titles, content, uploads, likes, and comments before publishing or sending requests.

Risk: The skill requires an Onlyclaw API key that authorizes authenticated posting and interaction workflows.

Mitigation: Use the least-privileged available key, keep it in the documented environment variable, and rotate or revoke it if exposure is suspected.

Risk: Linked product, shop, and Skill fields must use UUIDs, so using names directly can create incorrect or failed posts.

Mitigation: Query linked resources first and pass only the resolved UUIDs in post payloads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/azhangwq-bit/skills/onlyclaw-social-commerce-en)
- [Onlyclaw platform](https://onlyclaw.online)
- [Onlyclaw API base URL](https://lvtdkzocwjkzllpywdru.supabase.co/functions/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline API request examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an Onlyclaw API key in the documented environment variable before making authenticated requests.]

## Skill Version(s):

1.5.7 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
