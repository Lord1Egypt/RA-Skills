## Description:

Operate and improve the La Local location-management chat product across the frontend chat app, backend webhook, search behavior, media upload flow, Notion/Dropbox integration, deployment topology, and project-specific product logic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gatonegroialab](https://clawhub.ai/user/gatonegroialab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to maintain the La Local chat product, especially search, create/update flows, media uploads, and Notion/Dropbox integration. It guides agents to improve search without regressing deterministic record operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent work may involve Notion and Dropbox records for the La Local product.

Mitigation: Scope connected credentials appropriately and review create/update actions before applying them to production data.

Risk: Search changes could return invented, weak, or misleading location matches.

Mitigation: Retrieve candidates from source data, return only real matches, cap results at five, and verify ranking changes against real team queries.

Risk: Create/update regressions could break deterministic record handling or folder linkage.

Mitigation: Preserve thread_id, treat Notion as the source of truth, and keep Dropbox folder linkage tied to the Notion-generated ID.

## Reference(s):

- [Architecture](references/architecture.md)
- [Search Notes](references/search-notes.md)
- [La Local Chat Skill Page](https://clawhub.ai/gatonegroialab/skills/la-local-chat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional code, shell command, and configuration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Project-specific guidance; does not execute code directly.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
