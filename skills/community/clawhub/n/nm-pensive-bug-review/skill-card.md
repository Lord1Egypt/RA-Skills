## Description: <br>
Hunts bugs with evidence trails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review code for defects, document evidence with file and line references, prepare minimal fixes, and plan verification before releases, audits, or production issue investigations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review bundles may be sent to configured external reviewer CLIs or use web search. <br>
Mitigation: Use the skill only with repositories and data approved for the configured reviewer tools, and avoid external review paths for sensitive code. <br>
Risk: One optional reviewer path may rely on prompt instructions rather than enforced read-only controls. <br>
Mitigation: Prefer the default Codex path or engines with explicit read-only controls; manually review or harden the Droid engine before sensitive use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-pensive-bug-review) <br>
- [Pensive source homepage](https://github.com/athola/claude-night-market/tree/master/plugins/pensive) <br>
- [Language Detection](artifact/modules/language-detection.md) <br>
- [Defect Documentation](artifact/modules/defect-documentation.md) <br>
- [Fix Preparation](artifact/modules/fix-preparation.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with file references, code diffs, test updates, evidence, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed fixes and verification commands; users should review changes before applying them.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence; artifact frontmatter says 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
