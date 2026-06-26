## Description: <br>
Audit GitHub Actions rerun dependency and success-after-rerun effectiveness to highlight workflows wasting CI time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and CI maintainers use this skill to audit GitHub Actions run exports, quantify rerun dependency and recovery effectiveness, and optionally gate CI when critical rerun patterns appear. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitHub Actions exports and generated reports may include repository names, actors, branches, commit SHAs, and run URLs. <br>
Mitigation: Treat reports as internal CI metadata and share them only with authorized users. <br>
Risk: A broad RUN_GLOB can include unintended GitHub Actions export files. <br>
Mitigation: Scope RUN_GLOB to the intended export directory before running the audit. <br>
Risk: The skill can analyze CI data the operator is not authorized to review if supplied with those exports. <br>
Mitigation: Use the skill only with GitHub Actions exports the operator is allowed to analyze. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/github-actions-rerun-effectiveness-audit) <br>
- [Publisher profile](https://clawhub.ai/user/daniellummis) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bash examples; runtime reports are text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text mode prints summary and ranked workflow groups; JSON mode prints summary, ranked groups, all groups, and critical groups.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
