## Description: <br>
Orchestrates the QUALITY pipeline stage for egregore work items, running code review, unbloat, and test updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to run egregore QUALITY checks for work items and pull requests. It applies convention checks, invokes mapped review/refinement/test/documentation skills, collects findings, and records or posts a quality verdict. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send code diffs to external reviewer CLIs, and one optional reviewer path may not enforce the read-only isolation it describes. <br>
Mitigation: Use the default Codex path or engines with explicit read-only/tool-limited controls, avoid the Droid engine unless independently confirmed safe, and review findings or fixes before committing or posting them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-egregore-quality-gate) <br>
- [Metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/egregore) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce quality findings, pass or fix-required verdicts, suggested fixes, and PR review comments.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
