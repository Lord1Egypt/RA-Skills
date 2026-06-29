## Description: <br>
Evaluates Claude Code rules in .claude/rules/ for frontmatter validity, glob pattern quality, content quality, organization, and token efficiency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit Claude Code rule files for YAML frontmatter correctness, glob specificity, content quality, organization, and token efficiency before using them in projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect many repository documentation and instruction files and may suggest documentation-related edits in sensitive or private repositories. <br>
Mitigation: Review proposed findings and edits before applying them, especially when working with private repository content. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/athola/skills/nm-abstract-rules-eval) <br>
- [Clawdis Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/abstract) <br>
- [Frontmatter Validation](modules/frontmatter-validation.md) <br>
- [Glob Pattern Analysis](modules/glob-pattern-analysis.md) <br>
- [Content Quality Metrics](modules/content-quality-metrics.md) <br>
- [Organization Patterns](modules/organization-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown audit findings and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include scores, validation findings, and suggested edits for rule files.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
