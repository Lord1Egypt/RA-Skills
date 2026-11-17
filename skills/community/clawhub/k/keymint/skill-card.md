## Description:

Add software licensing to an app with Keymint. Choose a licensing model (node-locked, floating, offline, subscription), create and manage license keys, activate and deactivate devices, run floating (concurrent-seat) licenses, issue offline signed licenses, and manage customers through the Keymint REST API or official SDKs (Node.js, Python, Go, C#, PHP).

This skill is ready for commercial/non-commercial use.

## Publisher:

[keymint](https://clawhub.ai/user/keymint)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to select and integrate Keymint licensing for desktop apps, CLIs, plugins, and SaaS add-ons. It guides license and customer management through the Keymint API or official SDKs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented licensing workflows may send customer or device information to Keymint.

Mitigation: Review which customer and device fields the chosen workflow sends, and limit them to what the licensing flow needs.

Risk: The security scan had partial coverage because two local path-like references could not be resolved.

Mitigation: Resolve and review those references before relying on the scan's assessment.

## Reference(s):

- [Keymint documentation](https://keymint.dev/docs)
- [Keymint OpenAPI specification](https://keymint.dev/openapi.json)
- [Keymint API error codes](https://keymint.dev/docs/api-reference/error-codes)
- [Offline license verification](https://keymint.dev/docs/topics/offline-key)
- [Stripe subscription licensing guide](https://keymint.dev/docs/guides/stripe-subscription-licensing)
- [Keymint](https://keymint.dev)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell, JSON, and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
