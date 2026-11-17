## Description:

Capture and automate macOS UI with the Peekaboo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and macOS users use this skill to inspect applications, automate the intended interface, and verify the result with the Peekaboo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment is benign with medium confidence, but one referenced local path could not be resolved, leaving evidence incomplete.

Mitigation: Consider whether this evidence gap is acceptable before installing; a benign assessment does not mean risk-free.

Risk: UI actions may target the wrong application, window, or element if based on stale observations.

Mitigation: Inspect the current UI before acting, use the intended target, refresh observations when the window changes, and verify the result afterward.

## Reference(s):

- [Peekaboo homepage](https://peekaboo.boo)
- [ClawHub skill page](https://clawhub.ai/hillstreet-ph/skills/oc-peekaboo)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
