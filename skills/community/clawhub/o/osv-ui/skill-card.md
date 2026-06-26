## Description: <br>
Security auditing skill for scanning CVE vulnerabilities across npm, Python, Go, and Rust projects using osv-ui, opening a visual browser dashboard for human review, and applying fixes with explicit confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[toan203](https://clawhub.ai/user/toan203) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to scan npm, Python, Go, and Rust project dependencies for known vulnerabilities, review results in an OSV UI dashboard, and apply confirmed dependency fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs an external CLI through npx. <br>
Mitigation: Review the exact npx osv-ui command before execution. <br>
Risk: Dependency update commands can change project behavior. <br>
Mitigation: Require explicit confirmation before applying package updates and run normal tests after changes. <br>
Risk: The skill may activate on broad security requests. <br>
Mitigation: Confirm the user wants an osv-ui dependency scan before running commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/toan203/osv-ui) <br>
- [Publisher Profile](https://clawhub.ai/user/toan203) <br>
- [Project Homepage](https://github.com/toan203/osv-ui) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with inline shell commands and JSON or HTML report paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce OSV report artifacts such as osv-report.json or report.html through explicit commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
