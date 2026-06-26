## Description: <br>
Evaluates test suites for coverage gaps, TDD/BDD compliance, and anti-patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering reviewers use this skill to evaluate test suites for coverage gaps, framework fit, scenario quality, invariant-preserving tests, and remediation planning before releases or after failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may suggest running test, coverage, git, or package-install commands while inspecting a repository. <br>
Mitigation: Review commands before execution and approve package installs or coverage-report generation only in an appropriate workspace. <br>
Risk: Test quality recommendations may be incomplete or incorrect for large or sensitive repositories. <br>
Mitigation: Use the skill output as review guidance and require human validation before accepting remediation plans or release decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-pensive-test-review) <br>
- [OpenClaw metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/pensive) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review report with framework detection, coverage analysis, quality findings, remediation plan, and recommendation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include test, coverage, and git command suggestions for reviewer approval.] <br>

## Skill Version(s): <br>
1.9.12 (source: release evidence; artifact frontmatter says 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
