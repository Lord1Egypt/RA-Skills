## Description: <br>
Manage personal TODOs in Kan.bn through API-driven operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Wujiao233](https://clawhub.ai/user/Wujiao233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Kan.bn users use this skill to let an agent create, update, move, prioritize, search, summarize, and clean up personal TODO tasks through the Kan.bn API. It is scoped to single-user task-management workflows and excludes collaboration, invites, imports, integrations, and attachments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change or delete Kan.bn tasks and update personal task data. <br>
Mitigation: Require explicit confirmation before deletes, list deletion, profile updates, or ambiguous task matches, and prefer the narrowest matching operation. <br>
Risk: Kan.bn credentials authorize actions in the user's account. <br>
Mitigation: Use the least-privileged Kan.bn token available, verify KANBN_BASE_URL before use, and avoid ~/.bashrc credential discovery unless it is intentional. <br>


## Reference(s): <br>
- [Kan.bn TODO API Scope](references/api-scope.md) <br>
- [Common Kan.bn Workflows](references/common-workflows.md) <br>
- [Smoke Test](references/smoke-test.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Wujiao233/kanbn-todo-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with inline shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Kan.bn bearer-token or API-key authentication; actions are scoped to the configured Kan.bn API base URL.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
