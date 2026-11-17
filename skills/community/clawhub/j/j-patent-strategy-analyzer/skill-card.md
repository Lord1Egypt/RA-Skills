## Description:

Generates a template-driven enterprise patent strategy analysis by mapping company business information against global patent data and producing a standalone HTML report with inline CSS and charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent, IP, strategy, and consulting teams use this skill to turn uploaded Excel patent lists and researched company intelligence into a structured patent landscape, portfolio-quality, inventor, risk, gap, and action-plan report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs unpinned Python packages during report generation.

Mitigation: Run it in a managed or isolated environment and prefer a reviewed release with pinned dependency versions or hashes.

Risk: The workflow relies on a PatSnap/Zhihuiya account integration for patent and business intelligence inputs.

Mitigation: Use approved credentials and confirm that uploaded patent lists and retrieved intelligence are permitted for the intended use.

Risk: The workflow can create local recovery files or derived report data containing patent and business information.

Mitigation: Review retention requirements before use and remove local checkpoints, snapshots, and generated reports when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/j-patent-strategy-analyzer)
- [Zhihuiya open platform](https://open.zhihuiya.com/)
- [Data preparation specification](references/data_prep.md)
- [HTML report skeleton](references/html_skeleton.md)
- [Section filling specification](references/section_specs.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and HTML snippets that produces a standalone HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated report is intended to inline CSS and chart image data with no external runtime dependencies.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
