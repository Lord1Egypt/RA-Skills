## Description:

MakeX helps agents discover connected third-party service actions and execute them through OpenClaw Integrations API endpoints using organization-level authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tkejr](https://clawhub.ai/user/tkejr)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to discover available third-party integration actions, inspect account and action schemas, execute selected actions on connected accounts, and preview response structures for MakeX/OpenClaw workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An organization token can authorize server-to-server access to connected integrations.

Mitigation: Install or enable the skill only for trusted server-side callers, protect the org token like a production secret, and rotate or revoke it if exposed.

Risk: The run-action endpoint can execute live actions on connected third-party accounts, including actions that send messages or modify external systems.

Mitigation: Restrict which Composio actions and connected accounts may be used, and require explicit user confirmation before mutating external systems or sending messages.

Risk: The output-structure endpoint executes an action to inspect its response shape, which can cause side effects for some actions.

Mitigation: Avoid using output-structure on side-effecting actions; prefer read-only actions, sandbox accounts, or test data when previewing output shapes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tkejr/skills/makex)
- [MakeX](https://www.makex.app/)
- [OpenClaw Integrations API](artifact/SKILL.md)
- [Search Actions Endpoint](artifact/search-actions.txt)
- [Connected Account Endpoint](artifact/connected-account.txt)
- [Action Details Endpoint](artifact/action-details.txt)
- [Run Action Endpoint](artifact/run-action.txt)
- [Output Structure Endpoint](artifact/output-structure.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown documentation with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes endpoint descriptions, authentication requirements, request fields, response examples, and error cases.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
