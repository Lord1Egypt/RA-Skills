## Description:

Open Plantbook API workflows with schema-first plant search, detail, and user-plant writes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[slaxor505](https://clawhub.ai/user/slaxor505)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and agents use this skill to search Open Plantbook, retrieve plant detail and care fields, and create authenticated user plants through schema-checked API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use Open Plantbook credentials and make authenticated requests to open.plantbook.io.

Mitigation: Install it only for agents that should access Open Plantbook, keep unrelated secrets out of the optional env file, and use OAuth credentials only for write or sensor workflows.

Risk: Create, update, delete, and sensor upload workflows can change data in an external Open Plantbook account.

Mitigation: Review update/delete requests before approving them and require clear user intent before write actions.

Risk: Plant-care, toxicity, food-safety, medical, or veterinary conclusions may be incomplete if based only on Open Plantbook data.

Mitigation: Treat plant database output as informational care guidance and verify high-stakes safety claims with authoritative sources.

## Reference(s):

- [Open Plantbook documentation](https://open.plantbook.io/docs/)
- [Open Plantbook OpenAPI schema](https://open.plantbook.io/api/schema/)
- [Publish notes](references/publish-notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command examples when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May issue authenticated Open Plantbook API calls through the packaged helper or schema-aligned direct HTTP workflows.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata; artifact frontmatter metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
