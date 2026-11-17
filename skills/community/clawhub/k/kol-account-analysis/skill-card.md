## Description:

Analyzes a single public KOL or creator account to assess content consistency, audience reception, product-entry fit, collaboration formats, and risk boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qomob](https://clawhub.ai/user/qomob)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, creator partnerships, and brand teams use this skill to analyze one public KOL or creator account before collaboration. It helps convert public content and comment evidence into a reusable account understanding, collaboration-form recommendation, risk checklist, and evidence-boundary statement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can collect public comments into local files through browser automation.

Mitigation: Run collection in an isolated environment, use only public data, avoid login or session data, validate target URLs, and remove local exports when no longer needed.

Risk: Playwright-based collection may trigger platform rate limits or rely on changing page selectors.

Mitigation: Pin and review Playwright before use, keep collection rates low, and review or adapt selectors for the intended platform before running the collector.

Risk: Generated reports may include forced vendor branding when neutral reporting is required.

Mitigation: Review report templates before deployment and remove or make branding optional for neutral or client-facing deliverables.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qomob/skills/kol-account-analysis)
- [README](artifact/README.md)
- [Task Definition](artifact/references/task-definition.md)
- [Platform Context](artifact/references/platform-context.md)
- [Data Collection](artifact/references/data-collection.md)
- [Data Sources](artifact/references/data-sources.md)
- [Collection Playbook](artifact/references/collection-playbook.md)
- [Works Analysis](artifact/references/works-analysis.md)
- [Comments Analysis](artifact/references/comments-analysis.md)
- [Batch Processing](artifact/references/batch-processing.md)
- [Collaboration Judgment](artifact/references/collaboration-judgment.md)
- [Honest Boundaries](artifact/references/honest-boundaries.md)
- [Rules](artifact/references/rules.md)
- [Report Template](artifact/templates/report-template.md)
- [Trace Schema](artifact/trace-schema.json)
- [Verification Package](artifact/VERIFICATION.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown analysis report with optional CSV evidence files and shell commands for public-data collection]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public creator-account and comment evidence; conclusions are bounded by the stated evidence coverage.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
