## Description:

Describes product collection task HTTP APIs for creating, picking, updating, and batch-updating collection tasks, including task types, statuses, success payload rules, and browser-extension versus dashboard roles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rowin90](https://clawhub.ai/user/rowin90)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to integrate product collection workers, task queues, browser extensions, and dashboards with authenticated product task REST endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented create, update, and batch-update endpoints can change remote task or product data.

Mitigation: Scope PRODUCT_TASK_AUTH to the intended product-task environment and review request filters before using mutating endpoints.

Risk: Authorization headers could be exposed through logs, screenshots, chats, or hard-coded examples.

Mitigation: Read PRODUCT_TASK_AUTH from private configuration, avoid printing the full header, and keep real hostnames and secrets out of examples.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rowin90/skills/product-data-collection)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with endpoint tables, JSON body descriptions, and inline bash snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PRODUCT_TASK_AUTH and PRODUCT_DATA_COLLECTION_BASE_URL to be supplied out of band; documentation-only skill with no executable payloads.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
