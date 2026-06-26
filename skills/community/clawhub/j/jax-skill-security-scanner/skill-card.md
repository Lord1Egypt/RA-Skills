## Description: <br>
Scans OpenClaw skill folders for sensitive operations, backdoor patterns, prompt poisoning, hallucination, and misinformation risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jasonshieh](https://clawhub.ai/user/jasonshieh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to audit OpenClaw skills and generate text, Markdown, or JSON reports before installation, release, or CI use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner reads the selected skills folder and may surface sensitive local skill content in reports. <br>
Mitigation: Limit the scan path to the intended skills directory and review reports before sharing them. <br>
Risk: The scanner is heuristic and may miss risks or reduce risk scores based on weak name or path trust checks. <br>
Mitigation: Treat clean results and trust labels as advisory only, and pair them with manual review or an independent security scan before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jasonshieh/jax-skill-security-scanner) <br>
- [Publisher profile](https://clawhub.ai/user/jasonshieh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Text, Markdown, JSON, and enhanced report summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include risk levels, sensitive-operation findings, trojan-pattern summaries, and remediation suggestions.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
