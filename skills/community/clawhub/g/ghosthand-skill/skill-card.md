## Description:

Ghosthand guides agents operating a local Android control runtime exposed over a loopback HTTP API, including capability checks, screen inspection, selector planning, clicks, taps, text input, waits, screenshots, clipboard, and notification workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[folklore25](https://clawhub.ai/user/folklore25)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to control Android devices through Ghosthand's local HTTP routes while checking live runtime state and capabilities before acting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screen, clipboard, screenshot, and notification routes can expose sensitive Android device content.

Mitigation: Keep Ghosthand policy restrictions enabled, use sensitive routes only when the task requires them, and review captured content before sharing it.

Risk: Actions can fail or affect the wrong UI element if the agent relies on stale screen state or cached node IDs.

Mitigation: Read live state and screen data before acting, treat node IDs as snapshot-scoped, and re-resolve selectors after fresh observations.

Risk: A route may be unavailable when Android authorization or Ghosthand policy does not allow its capability.

Mitigation: Check `/state`, and use `/capabilities` when capability availability or route mapping is ambiguous.

## Reference(s):

- [Ghosthand API Quick Reference](resources/references/ghosthand-api-quick-reference.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls]

**Output Format:** [Markdown guidance with inline HTTP route examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
