## Description:

Manage personal TODOs in Kan.bn through API-driven operations for creating, updating, moving, prioritizing, searching, summarizing, and cleaning up single-user board data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wujiao233](https://clawhub.ai/user/wujiao233)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let an agent manage their personal Kan.bn tasks through authenticated single-user TODO workflows, including discovery, creation, updates, moves, priority labels, comments, checklists, search, and cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured Kan.bn credentials can be sent to a non-default API server if the base URL is changed.

Mitigation: Use the default Kan.bn API URL unless the endpoint is fully trusted, and avoid custom base URLs for routine use.

Risk: Delete commands can remove cards, lists, comments, or checklist items.

Mitigation: Require exact targets and explicit confirmation before destructive operations.

Risk: The skill uses credentials that may allow reads and writes to personal Kan.bn board data.

Mitigation: Use only credentials the user is comfortable letting an agent use, and stop early when the auth source is missing or unclear.

## Reference(s):

- [Kan.bn TODO API Scope](references/api-scope.md)
- [Common Kan.bn Workflows](references/common-workflows.md)
- [Smoke Test](references/smoke-test.md)
- [Kan.bn API Base URL](https://kan.bn/api/v1)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Kan.bn bearer token or API key; supports read and write task-management operations against a configurable API base URL.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
