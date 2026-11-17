## Description:

Audit a Next.js App Router codebase for React Server Component boundary mistakes, request waterfalls, client/server anti-patterns, and Core Web Vitals risks, then propose concrete fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sioncoolwijk](https://clawhub.ai/user/sioncoolwijk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit Next.js App Router projects for high-impact correctness, SEO, security, and performance issues. It combines a local static scanner with a manual review checklist and returns prioritized findings with concrete fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent and scanner need to read the Next.js project source selected for audit.

Mitigation: Run the skill only on projects whose source may be reviewed by the agent, and avoid pointing it at unrelated sensitive repositories.

Risk: Scanner findings are heuristic leads and may include false positives or incomplete diagnoses.

Mitigation: Confirm each finding against the source code and project intent before applying fixes or treating the issue as resolved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sioncoolwijk/skills/nextjs-app-router-audit)
- [App Router review checklist](reference/checklist.md)
- [Sample audit report](examples/sample-report.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown audit report with file:line findings, severity, impact, fixes, score, and optional JSON scanner output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled scanner is local and read-only, exits non-zero when ERROR findings exist, and produces heuristic leads that should be verified against source code.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
