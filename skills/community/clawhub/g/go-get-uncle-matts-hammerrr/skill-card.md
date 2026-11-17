## Description:

Go Get Uncle Matt's HAMMERRR is a read-only project-truth audit skill that reconciles project claims with reachable runtime behavior, configuration, deployment reality, tests, executable proof, and release paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uncmatteth](https://clawhub.ai/user/uncmatteth)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill when they need an explicit, evidence-heavy audit of whether project documentation, configuration, tests, runtime behavior, packaging, and release paths match reality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to inspect broad project files and run read-only local checks during an audit.

Mitigation: Use it only for explicit, evidence-heavy project audits and review any proposed live probe or command before allowing execution.

Risk: The bundled validator currently fails because it expects a packaging file that is not present in this release.

Mitigation: Treat validator failure as a packaging issue for the maintainer to resolve by adding the missing file or updating the validator.

Risk: Audit output may include proposed commands or next proof steps that require human judgment before execution.

Mitigation: Keep the default audit flow read-only and require reviewer approval before dependency installation, publishing, deployment, credential access, or other mutating operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/uncmatteth/skills/go-get-uncle-matts-hammerrr)
- [Claim Model](references/claim-model.md)
- [Evidence Rules](references/evidence-rules.md)
- [Command Safety](references/command-safety.md)
- [Reality Gap Checklist](references/reality-gap-checklist.md)
- [Report Rules](references/report-rules.md)
- [Project Truth Audit Schema](schemas/project-truth-audit.schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, shell commands]

**Output Format:** [Markdown audit report, with optional JSON report and optional Markdown remediation plan when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only by default; includes evidence, proof status, confidence, findings, rejected suspicions, blockers, and next proof steps.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
