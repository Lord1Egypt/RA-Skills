# Knowledge Sources

## Confirmed

Use sources according to the decision being made.

### Project-Local Evidence

Check the repository before relying on general assumptions:

- `AGENTS.md`
- `CLAUDE.md`
- `SKILL.md`
- `CONTRIBUTING.md`
- `README.md`
- `.github/copilot-instructions.md`
- `.github/instructions/*`
- Source code, tests, build configuration, Git history, issues, and review discussion

When rules conflict, prefer the more specific rule located closer to the files being changed.

### Primary Technical Sources

Prefer:

- Official documentation
- Specifications and standards
- Upstream source code
- Maintainer documentation and release notes
- Reproducible tests, benchmarks, logs, and minimal experiments
- Public repository metadata and remote HEAD information

Authority is useful context, not final proof.

### Security Sources

Use:

- Reproduction evidence
- Maintainer security channels
- Advisories and vulnerability databases
- Independent corroboration
- Impact and exploitability analysis

Do not treat an anonymous report, AI confidence score, or unverified suspicion as a confirmed vulnerability. A technically plausible signal may justify temporary containment and further investigation.

### AI As A Source

Use AI to:

- Generate hypotheses
- Explain unfamiliar code
- Search for independent evidence
- Cross-check reasoning
- Identify high-risk paths
- Suggest experiments and mitigations

Do not use AI confidence as evidence by itself. Keep final responsibility with the human who approves the action.

Do not expose raw sensitive data to external AI when adequate privacy cannot be preserved. Prefer minimization, anonymization, synthetic samples, local analysis, or manual investigation.

### Community And User Evidence

Use:

- Actual usage
- Retention
- Issue patterns
- User impact
- Migration cost
- Community votes
- Feedback from deeply dependent users

Do not equate stars, registrations, or discussion volume with durable value without additional evidence.

## Strong Inference

- Prefer multiple independent sources for high-impact conclusions.
- Match research effort to consequence: lightweight checks for reversible experiments, deeper verification for Security, payment, privacy, and data integrity.
- Treat community votes as input rather than permission to ignore concentrated harm to minority users.
- Prefer observable behavior over self-description when evaluating collaborator reliability.

## Unknown

- Preferred named news sources, blogs, forums, researchers, or technical publications.
- Preferred security advisory databases and disclosure coordinators.
- Whether social-media reports should ever be treated as sufficient evidence outside emergency containment.
- Preferred metrics for product retention, growth quality, and long-term project value.
