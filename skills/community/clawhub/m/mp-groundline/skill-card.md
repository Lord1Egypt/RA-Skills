## Description:

Helps developers migrate a WeChat Mini Program from Skyline to WebView while preserving page behavior and producing a migration map.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentjiang06](https://clawhub.ai/user/vincentjiang06)

### License/Terms of Use:

MIT-0

## Use Case:

Developers migrating WeChat Mini Programs from Skyline to WebView use this skill to inventory compatibility issues, plan minimal changes, and verify affected pages before finalizing the migration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner can be steered to read files outside the selected project.

Mitigation: Run it only on trusted projects; check that miniprogramRoot stays within the project before scanning.

Risk: Migration edits may change page behavior or require manual rewrites.

Mitigation: Use a pinned release on a clean git tree and review the MIGRATION-MAP before edits.

Risk: Before/after capture may include sensitive app content.

Mitigation: Avoid sensitive live sessions during capture, and mark pages unverified if verification cannot run.

## Reference(s):

- [mp-groundline on ClawHub](https://clawhub.ai/vincentjiang06/skills/mp-groundline)
- [Skyline to WebView migration map](references/skyline-to-webview.md)
- [Scanner contract](references/scanner-contract.md)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Code, Configuration guidance]

**Output Format:** [JSON scan findings, a Markdown migration map, and targeted project edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Marks pages unverified when before/after capture is unavailable.]

## Skill Version(s):

0.2.3 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
