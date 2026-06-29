## Description: <br>
Scores backlog items with RICE, WSJF, and Kano methods, then prepares GitHub issues for selected top candidates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product engineers, and roadmap reviewers use this skill to inventory implemented features, score backlog candidates, compare tradeoffs, and decide which suggestions should become GitHub issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run a local Python deferred-capture script automatically for skipped high-priority suggestions. <br>
Mitigation: Inspect or remove the deferred-capture behavior before deployment, or require an explicit user confirmation before any local script execution. <br>
Risk: GitHub issue creation can publish roadmap suggestions or prioritization details outside the local review context. <br>
Mitigation: Keep issue-creation confirmation enabled and review generated issue titles, bodies, labels, and related links before submission. <br>
Risk: Research-enriched scoring may use external research channels when the --research option is enabled. <br>
Mitigation: Use --research only when sharing feature topics with external research sources is acceptable for the project. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-imbue-feature-review) <br>
- [OpenClaw homepage metadata](https://github.com/athola/claude-night-market/tree/master/plugins/imbue) <br>
- [Scoring framework](artifact/modules/scoring-framework.md) <br>
- [Classification system](artifact/modules/classification-system.md) <br>
- [Tradeoff dimensions](artifact/modules/tradeoff-dimensions.md) <br>
- [Research enrichment](artifact/modules/research-enrichment.md) <br>
- [Configuration](artifact/modules/configuration.md) <br>
- [Multi-metric evaluation methodology](artifact/modules/multi-metric-evaluation-methodology.md) <br>
- [External multi-metric methodology reference](https://claude-night-market/plugins/abstract/skills/skills-eval/modules/multi-metric-evaluation-methodology.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, tables, GitHub issue drafts, command suggestions, and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can optionally include research evidence and GitHub issue metadata when requested.] <br>

## Skill Version(s): <br>
1.9.13 (source: ClawHub release metadata; artifact frontmatter reports 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
