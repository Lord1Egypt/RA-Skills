## Description:

Moments GEO Skills helps agents run GEO and AIEO workflows for brand visibility diagnostics, positioning, AI-optimized content creation, question libraries, and ongoing monitoring across AI search platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenerlee](https://clawhub.ai/user/kenerlee)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing teams, consultants, and brand operators use this skill to assess and improve how a brand appears in AI-generated search and recommendation answers. It guides agents through audits, positioning work, content planning, schema recommendations, and recurring visibility reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can drive broad browser, network, and local file activity while producing client reports.

Mitigation: Run it in a bounded workspace, restrict audits to authorized public HTTPS sites, and review generated files before sharing them.

Risk: Unsafe shell and URL-fetch patterns may be exposed to untrusted brand names, paths, or URLs.

Mitigation: Treat brand names, URLs, and file paths as untrusted input; avoid passing them directly into shell commands and verify destinations before fetching.

Risk: Logged-in AI/browser sessions and client materials can expose sensitive business data.

Mitigation: Use dedicated browser profiles or accounts, avoid entering secrets, and remove proprietary data from prompts and logs unless explicitly authorized.

Risk: AI visibility reports can mislead clients if estimated platform results are presented as measured results.

Mitigation: Use real platform testing when available; otherwise label estimates clearly and include methodology notes and limitations in reports.

## Reference(s):

- [GEO-Claw Skill Definition](SKILL.md)
- [GEO Deployment Template](references/template-geo.md)
- [Phase 1 Diagnosis Workflow](references/phase1-diagnosis-full.md)
- [Phase 2 Positioning Workflow](references/phase2-positioning-full.md)
- [Phase 3 Content Workflow](references/phase3-content-full.md)
- [Phase 4 Monitoring Workflow](references/phase4-monitoring-full.md)
- [Question Library](references/question-library.md)
- [AI Platform Specifications](references/ai-platform-specs.md)
- [Content Guidelines](references/content-guidelines.md)
- [Monitoring Metrics](references/monitoring-metrics.md)
- [Tools Guide](references/tools-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, tables, JSON-LD snippets, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local client reports, content plans, question libraries, schema recommendations, and analysis outputs; AI-platform test results must be labeled as measured or estimated based on available tooling.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
