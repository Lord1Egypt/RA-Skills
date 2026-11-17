## Description:

Autonomous inventory management and waste reduction agent for QSRs that cross-references sales data with inventory levels to forecast ordering, flag excessive waste, and use ThumbGate checks to prevent over-ordering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[igorganapolsky](https://clawhub.ai/user/igorganapolsky)

### License/Terms of Use:

MIT-0

## Use Case:

QSR operators and inventory teams use this skill to monitor sales and inventory sheets, identify waste patterns, generate restock recommendations, and block abnormal purchase workflows that exceed configured ThumbGate thresholds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup asks users to execute an unpinned third-party ThumbGate npm package.

Mitigation: Verify the package name, publisher, repository, and version before installation, then run a pinned reviewed version in a least-privilege environment.

Risk: The skill may need access to business inventory, sales, ordering, or purchase-order workflows.

Mitigation: Connect only the required Google Sheets, prefer read-only access unless write actions are intentionally needed, and require human approval for purchases or manual overrides.

## Reference(s):

- [Setup Guide](artifact/setup-guide.md)
- [ThumbGate Prevention Rules](artifact/thumbgate-rules.md)
- [Make.com](https://make.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and operational recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes restock recommendations, waste flags, alert-routing setup, and ThumbGate guardrail guidance.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
