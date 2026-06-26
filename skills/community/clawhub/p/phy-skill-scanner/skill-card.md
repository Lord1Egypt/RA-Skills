## Description: <br>
Pre-install security scanner for ClawHub skills that analyzes SKILL.md files for prompt injection, data exfiltration patterns, malicious shell commands, typosquatting, and quality red flags before installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and team administrators use this skill to review ClawHub skill files before installation or deployment. It produces a heuristic security and quality assessment to guide install, skip, or further-review decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat heuristic scanner results as a guarantee that a skill is safe. <br>
Mitigation: Use the report as review guidance, provide only the skill content intended for inspection, and combine the result with ClawHub's built-in scanning and human review for higher-risk installs. <br>
Risk: The scanner may miss obfuscated instructions or malicious URL destinations. <br>
Mitigation: Review encoded or unclear content manually, verify linked URLs separately, and escalate suspicious findings before installing or deploying the inspected skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-skill-scanner) <br>
- [Canlah AI homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown security audit report with scoring table, verdict, issues, and recommendation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports full, quick-scan, and batch report variants.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
