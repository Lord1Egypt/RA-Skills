## Description:

Use when working with JoggAI v2 APIs and workflow execution for avatar videos, product videos, templates, assets, avatars, webhooks, translation, and account lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joggai-tech](https://clawhub.ai/user/joggai-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to route JoggAI v2 API requests, run supported video and asset workflows, check account or quota information, and retrieve asynchronous job results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can call JoggAI account APIs using JOGG_API_KEY.

Mitigation: Install it only when the agent should use that key, and review user-directed API requests before execution.

Risk: Supported workflows can upload local media, create videos, and create, update, or delete webhooks in the JoggAI account.

Mitigation: Confirm file paths, payloads, webhook targets, and requested account actions before running those workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joggai-tech/skills/jogg-api)
- [Server-resolved GitHub source](https://github.com/JoggAI-Tech/jogg-skills/tree/main/skills/jogg-api)
- [Jogg API base URL](https://api.jogg.ai)

## Skill Output:

**Output Type(s):** [json, shell commands, configuration, guidance]

**Output Format:** [Machine-readable JSON on stdout with progress logs on stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, a shell environment, and JOGG_API_KEY; polling is bounded by interval, wait, and attempt limits.]

## Skill Version(s):

0.1.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
