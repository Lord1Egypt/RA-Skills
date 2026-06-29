## Description: <br>
Improves code quality across duplication, efficiency, and architectural fit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect existing code for duplication, inefficient algorithms, clean-code issues, and architectural mismatches, then produce prioritized refactoring plans and optional code changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Aggressive execution instructions can push the agent beyond planning into code changes when execution modes are requested. <br>
Mitigation: Run the skill in plan-only mode by default, require explicit approval before applying changes, and review diffs plus tests before merge. <br>
Risk: The insight-generation module can post refinement findings to GitHub Discussions, which may expose repository details or proprietary information. <br>
Mitigation: Do not run insight generation unless external posting is intended; inspect findings for secrets, sensitive paths, and proprietary code details before posting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-pensive-code-refinement) <br>
- [Project homepage from metadata](https://github.com/athola/claude-night-market/tree/master/plugins/pensive) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown reports with YAML-style finding records, inline shell commands, and optional code changes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are prioritized by impact, effort, and risk; the insight-generation module can post selected findings externally if run.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata; artifact frontmatter reports 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
