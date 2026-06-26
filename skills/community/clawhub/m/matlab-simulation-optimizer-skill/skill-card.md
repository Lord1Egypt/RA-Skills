## Description: <br>
Audit and optimize MATLAB simulation programs against a corresponding academic paper or specification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[orbisz](https://clawhub.ai/user/orbisz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to compare MATLAB simulation source with a reference paper or specification, fix fidelity issues, optimize runtime without changing required algorithm behavior, and produce a Chinese modification summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can directly edit MATLAB source files, remove code it judges unused, and write summary or scan-output files. <br>
Mitigation: Use version control, review diffs before relying on results, and request an analysis-only or patch-preview pass when working in sensitive projects. <br>
Risk: The release evidence flags self-maintenance diary and SKILL.md change instructions that go beyond the normal MATLAB optimization task. <br>
Mitigation: Ignore or remove self-evolution diary and skill-maintenance instructions unless the user explicitly wants the skill to maintain its own notes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/orbisz/matlab-simulation-optimizer-skill) <br>
- [MATLAB audit checklist](references/matlab-audit-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, code, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries, source-code edits, traceability tables, and optional JSON scan output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write optimization_summary.md and matlab_static_scan.json in the target MATLAB project when requested or useful.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
