## Description:

Use when integrating Outlit tracking into web, server, native, or desktop apps; adding SDK event tracking, identity, consent, activation configuration, billing integrations, visitor tracking, customerId attribution, or troubleshooting @outlit/browser, @outlit/node, or the Rust outlit crate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leo-paz](https://clawhub.ai/user/leo-paz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add or troubleshoot Outlit analytics instrumentation across browser, server, native, and desktop applications, including identity, consent, activation, billing, and event tracking decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead agents to enable broad automatic visitor, form, and identity tracking in the target app.

Mitigation: Review consent, auto-tracking, user disclosure, data retention, and sensitive-field handling before deploying instrumentation.

Risk: The skill may guide use of persistent fingerprints, email, userId, or customerId values for attribution.

Mitigation: Collect the minimum identifiers needed, align identity choices with privacy policy and consent requirements, and avoid sending secrets or unnecessary personal data.

Risk: The installation guidance includes an unpinned global npx command.

Mitigation: Prefer a pinned, local, or isolated install path before using the skill in production environments.

## Reference(s):

- [Outlit skill page](https://clawhub.ai/leo-paz/skills/outlit-sdk)
- [Outlit quickstart](https://docs.outlit.ai/tracking/quickstart)
- [Outlit tracking concepts](https://docs.outlit.ai/tracking/how-it-works)
- [Outlit customer context graph](https://docs.outlit.ai/concepts/customer-context-graph)
- [Outlit browser SDK](https://docs.outlit.ai/tracking/browser/npm)
- [Outlit Node.js SDK](https://docs.outlit.ai/tracking/server/nodejs)
- [Outlit Rust SDK](https://docs.outlit.ai/tracking/server/rust)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include framework-specific installation, initialization, identity, consent, event tracking, and troubleshooting steps.]

## Skill Version(s):

1.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
