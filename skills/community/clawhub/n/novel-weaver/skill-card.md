## Description: <br>
Novel Weaver helps agents run a structured novel-writing workflow with scene setup, outline generation, causal checks, gated chapter planning, continuity review, style checks, logic checks, fidelity checks, ending verification, entity tracking, character alias recognition, and cross-chapter behavior summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ldxs001](https://clawhub.ai/user/ldxs001) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and writing-focused agents use this skill to plan, draft, validate, and revise long-form fiction through a staged workflow with local project state, chapter files, continuity gates, and optional local semantic or reasoning checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and updates persistent local novel project state, chapter files, reports, and a current-project cache. <br>
Mitigation: Install and run it only when a persistent local writing workflow is desired, and review the configured project data directory before use. <br>
Risk: Optional model setup commands download third-party packages or models, and one optional command enables remote model code. <br>
Mitigation: Run optional model setup only from trusted sources, preferably in an isolated environment, and treat it as a separate trust decision. <br>


## Reference(s): <br>
- [Novel Weaver Skill Page](https://clawhub.ai/ldxs001/skills/novel-weaver) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Execution Standards](artifact/references/execution_standards.md) <br>
- [Workflow Hooks](artifact/references/hooks.md) <br>
- [Examples](artifact/references/examples.md) <br>
- [FAQ](artifact/references/faq.md) <br>
- [Permissions](artifact/references/permissions.md) <br>
- [Changelog](artifact/references/changelog.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON project state, text chapter drafts, and local report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local project state, chapter text, gate status, continuity reports, style reports, logic reports, fidelity reports, and ending verification reports.] <br>

## Skill Version(s): <br>
1.35.2 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
