## Description: <br>
HaluCatch audits AI skill packages for execution reliability, reproducibility, business-rule clarity, and interpretation guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codermoray](https://clawhub.ai/user/codermoray) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, skill authors, and engineering reviewers use HaluCatch to scan a target Skill directory, classify its reliability profile, and produce review reports with fix guidance before release or reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill recursively inspects the selected folder and writes local markdown reports, so broad paths may include unrelated or sensitive files. <br>
Mitigation: Run it only on an intentional Skill directory, avoid home, root, secrets, and broad project folders unless that scan is intended, and review generated reports before sharing. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/codermoray/skills/halucatch) <br>
- [HaluCatch README](README.md) <br>
- [HaluCatch FAQ](FAQ.md) <br>
- [HaluCatch Online Site](https://codermoray.github.io/HaluCatch/) <br>
- [HaluCatch Decision Flowchart](https://codermoray.github.io/HaluCatch/decision-flowchart.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with optional inline shell commands and fix guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local report files and can run validate-only scans for a selected Skill directory.] <br>

## Skill Version(s): <br>
1.7.7 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
