## Description:

Office Link helps agents link and manage third-party accounts through MorphixAI and call third-party APIs through a proxy when no dedicated skill exists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paul-leo](https://clawhub.ai/user/paul-leo)

### License/Terms of Use:


## Use Case:

Developers and operators use Office Link to check linked accounts, start OAuth account linking, and route calls to supported third-party APIs when a dedicated platform skill is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The proxy can call APIs in linked third-party accounts, including operations that create, update, delete, post, or otherwise change external data.

Mitigation: Require explicit user approval before any state-changing proxy call, and prefer dedicated platform skills when they are available.

Risk: Broad API-key scopes and linked-account access may exceed what a specific task needs.

Mitigation: Use the minimum API-key scopes available, avoid blanket all-scope keys when possible, and review or pin the MorphixAI plugin source and version before installation.

Risk: Users may link sensitive third-party accounts through an external account-linking service.

Mitigation: Install only when the MorphixAI plugin source is trusted and account owners are comfortable granting the requested third-party access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paul-leo/skills/mx-link)
- [MorphixAI API keys](https://morphix.app/api-keys)
- [MorphixAI connections](https://morphix.app/connections)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline command, JSON, and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MORPHIXAI_API_KEY and linked third-party accounts for live account-management or proxy operations.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
