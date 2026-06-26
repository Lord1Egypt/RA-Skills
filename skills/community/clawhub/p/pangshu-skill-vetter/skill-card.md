## Description: <br>
Security vetting for agent skills before installation that scans skill code for dangerous Bash commands, sensitive file access, network exfiltration, obfuscated code, and other security risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hjshysst-dot](https://clawhub.ai/user/hjshysst-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to scan agent skill directories before installation or update. It helps identify critical, warning, and informational findings and produces an install verdict for local review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A clean scan result may miss risks outside the heuristic patterns this skill checks. <br>
Mitigation: Treat clean results as useful signal rather than a guarantee, and review skill behavior before deployment. <br>
Risk: Automatic install hooks can read files from configured skill paths. <br>
Mitigation: Keep hooks scoped to incoming skill packages and scan explicit paths only. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hjshysst-dot/pangshu-skill-vetter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style security report with severity counts, findings, and a verdict] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are grouped as critical, warning, or info; command exit codes reflect the highest observed severity.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
