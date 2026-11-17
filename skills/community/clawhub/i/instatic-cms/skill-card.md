## Description:

Install, build, design, publish with Instatic (self-hosted visual CMS): canvas, collections, templates, tokens, agent, MCP. Trigger: instatic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cbertucci33](https://clawhub.ai/user/cbertucci33)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to install, administer, automate, and verify a self-hosted Instatic CMS instance, including content models, publishing, styling, API workflows, MCP access, and plugins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through broad CMS administration, including schema changes, publishing, plugin lifecycle operations, user management, credentials, personal access tokens, provider keys, and step-up passwords.

Mitigation: Install it only for agents that should help operate your own Instatic instance, treat secrets as sensitive, and confirm destructive or public-facing changes before execution.

Risk: Schema, import, plugin, user, and publish operations can change or expose live site state.

Mitigation: Keep backups before these operations, use the documented step-up flow, and verify changes by reading back stored state and fetching published HTML.

Risk: Instatic behavior may drift from the v0.0.20 source used to compile the skill.

Mitigation: Verify behavior against the pinned checkout and the live instance before relying on route, capability, field, migration, or publishing details.

Risk: Loop-bearing pages may publish with server-filled holes that are not suitable for a pure static host.

Mitigation: Fetch published pages and count instatic-hole occurrences before promising static-host compatibility.

## Reference(s):

- [Instatic upstream repository](https://github.com/corebunch/instatic)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [Instatic CMS skill page](https://clawhub.ai/cbertucci33/skills/instatic-cms)
- [Instatic Admin API Reference](artifact/instatic-cms/api.md)
- [Verification](artifact/instatic-cms/verification.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with inline commands, endpoint details, configuration notes, and verification checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pure-documentation skill; outputs should be checked against the operator's pinned Instatic version and live instance state.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
