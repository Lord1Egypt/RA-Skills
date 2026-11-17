## Description:

Cnc Quick Probe helps an agent collect missing CNC quote parameters and route the request once material, quantity, tolerance, surface treatment, and roughness are sufficiently complete.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timo2026](https://clawhub.ai/user/timo2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and quoting agents use this skill when a CNC quote request lacks enough information. It asks for five quote-critical parameters, tracks convergence, and prepares the request for downstream quotation once the threshold is met.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill imports executable Python from a hard-coded local cnc-quote-system path that is not bundled or integrity-checked.

Mitigation: Install only in environments where that dependency path is controlled, trusted, immutable, and reviewed before use.

Risk: CNC quote readiness depends on user-provided parameters and convergence state.

Mitigation: Have a qualified reviewer confirm collected material, quantity, tolerance, surface treatment, and roughness before relying on the resulting quote workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/timo2026/skills/openclaw-cnc-quick-probe)
- [Publisher profile](https://clawhub.ai/user/timo2026)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown prompts with structured status fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes convergence status, current CNC parameters, follow-up questions, and readiness to route for quotation.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and code report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
