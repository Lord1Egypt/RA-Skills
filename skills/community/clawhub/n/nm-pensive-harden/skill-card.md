## Description: <br>
Applies NIST/CWE security hardening to Python and Rust code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to run repo-wide security-posture audits before releases, after dependency changes, or when onboarding a repository. It inventories the codebase, maps findings to NIST SSDF and CWE references, and drafts approval-gated remediation proposals for Python, Rust, dependencies, CI, secrets, containers, and frontier security concerns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has broad activation triggers and performs repo-wide inspection across CI, dependencies, secrets posture, containers, and related configuration. <br>
Mitigation: Install it only where that audit scope is intended, and review its hardening report before approving any remediation proposal. <br>
Risk: Remediation proposals can change security-sensitive code or configuration. <br>
Mitigation: Use the built-in approval gate, keep one finding per commit, re-run project gates after each approved change, and rely on the recorded reversal plan when a change fails validation. <br>
Risk: An auto-apply option can reduce human review for lower-severity findings. <br>
Mitigation: Keep auto-apply disabled unless the repository has already reviewed the skill's reports and limit any auto-apply threshold to findings the team is comfortable reverting. <br>


## Reference(s): <br>
- [Nm Pensive Harden on ClawHub](https://clawhub.ai/athola/skills/nm-pensive-harden) <br>
- [Publisher Profile](https://clawhub.ai/user/athola) <br>
- [Clawdis Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/pensive) <br>
- [NIST and CWE Citation Backbone](artifact/modules/nist-controls.md) <br>
- [Proposal Shape](artifact/modules/proposal-shape.md) <br>
- [Cross-Cutting Hardening Checks](artifact/modules/cross-cutting.md) <br>
- [Python Hardening Checks](artifact/modules/python-checks.md) <br>
- [Rust Hardening Checks](artifact/modules/rust-checks.md) <br>
- [Frontier Hardening Checks](artifact/modules/frontier-checks.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with findings tables, remediation proposals, diffs or configuration snippets, and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings include severity, citation, file location, disposition, blast radius, reversal plan, and expected validation test when applicable.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence; artifact frontmatter reports 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
