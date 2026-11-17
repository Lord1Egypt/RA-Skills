## Description:

GTS Operator lets an AI agent manage a GTS multi-tenant forms and approval platform through dynamically discovered REST APIs, including tenant setup, organization and user maintenance, form and workflow configuration, approval actions, delegation, timeout handling, querying, export, and template sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dengkane](https://clawhub.ai/user/dengkane)

### License/Terms of Use:

MIT-0

## Use Case:

Tenant administrators, operations teams, and developers use this skill to configure and operate GTS tenants, users, forms, workflows, approvals, delegation, timeout rules, exports, and template sharing through conversation-driven API actions. It is intended for normal ClawHub release use against trusted GTS environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store a powerful 30-day GTS access token in ~/.gts-operator.json.

Mitigation: Install only for trusted GTS endpoints, use a controlled machine and agent profile, protect or remove the token file after use, and revoke authorization when finished.

Risk: The skill can perform high-impact business workflow actions, including deletion, public template publishing, approval decisions, and automatic approve or reject rules.

Mitigation: Require clear user confirmation before sensitive or destructive actions, public publishing, approval actions, and timeout rules that automatically approve or reject.

Risk: Public template market publishing can expose a tenant's template configuration to other tenant administrators.

Mitigation: Preview and summarize the template contents before publishing, confirm the public visibility with the user, and require confirmation before unlisting templates.

Risk: Timeout approve or reject behavior can create machine-generated approval outcomes without direct human action at execution time.

Mitigation: Keep automatic approval outcomes explicit and opt-in, require acknowledged confirmation before writing those rules, and describe audit records as rule-generated outcomes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dengkane/skills/gts-operator)
- [GTS API endpoint](https://www.geeyo.com/s/gts/api.php)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, markdown]

**Output Format:** [Natural-language guidance with API request details, JSON configuration examples, and concise status summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist a GTS OAuth token locally for up to 30 days when the user authorizes device-flow access.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
