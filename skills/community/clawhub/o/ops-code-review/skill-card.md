## Description: <br>
Ops Code Review automates SVN-based code review and security scanning for Django/Python, React with TypeScript, PHP, and mixed repositories, then generates Feishu-ready reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freepengyang](https://clawhub.ai/user/freepengyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to scan changed or full SVN repositories, check multi-language code with linters and security tools, and produce actionable reports for code review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency installation can modify the host environment, including system packages or global language tooling. <br>
Mitigation: Install and run the skill only in a dedicated or containerized environment, avoid install-deps on production or shared hosts, and provision dependencies through trusted pinned packages where possible. <br>
Risk: SVN password handling may expose credentials during scans. <br>
Mitigation: Use a least-privileged read-only SVN account and fix the SVN password argv handling before using the skill in CI, hooks, or multi-user systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freepengyang/ops-code-review) <br>
- [Publisher profile](https://clawhub.ai/user/freepengyang) <br>
- [React TypeScript ESLint reference](references/eslint.react.ts.js) <br>
- [Composer installer](https://getcomposer.org/installer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration JSON examples, and generated scan reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces incremental or full scan reports and can write local JSON report and message files during execution.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
