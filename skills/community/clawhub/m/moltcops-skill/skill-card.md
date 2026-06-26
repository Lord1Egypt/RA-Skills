## Description: <br>
Pre-install security scanner for AI agent skills. Detects malicious patterns before you trust code. Local-first — code never leaves your machine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Adamthompson33](https://clawhub.ai/user/Adamthompson33) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill before installing or running AI agent skills to scan local skill folders for prompt injection, code injection, data exfiltration, hardcoded secrets, and related threat patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner reads files from folders selected by the user during local scans. <br>
Mitigation: Run it only on intended skill directories and review the selected path before execution. <br>
Risk: Rule matches may be incomplete or may flag benign code as suspicious. <br>
Mitigation: Treat PASS/WARN/BLOCK results as advisory and manually review findings before installing or rejecting a skill. <br>


## Reference(s): <br>
- [MoltCops web scanner](https://scan.moltcops.com) <br>
- [MoltCops website](https://moltcops.com) <br>
- [MoltCops Moltbook profile](https://moltbook.com/u/MoltCops) <br>
- [ClawHub skill page](https://clawhub.ai/Adamthompson33/moltcops-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Shell commands, Guidance] <br>
**Output Format:** [Terminal text with PASS/WARN/BLOCK verdicts and finding summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit codes indicate PASS, WARN, or BLOCK; findings are advisory and should be reviewed before acting.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
