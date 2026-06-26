## Description: <br>
GraphQL anti-pattern and security analyzer that detects query depth and complexity issues, resolver N+1 problems, over- and under-fetching, rate limiting and auth gaps, schema design issues, and client query safety problems in GraphQL codebases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to run local GraphQL quality and security scans, review findings, and produce text, JSON, HTML, or Markdown reports for remediation and CI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local shell scripts and optional git-hook installation can create persistent repository behavior. <br>
Mitigation: Review the scripts before use, run scans against explicit target paths, and install hooks only in repositories where commit and push scanning is intended. <br>
Risk: License keys are sensitive and may be exposed if passed through command-line arguments or untrusted token sources. <br>
Mitigation: Prefer the GQLLINT_LICENSE_KEY environment variable or the documented OpenClaw configuration file, and avoid using untrusted license tokens. <br>
Risk: The scanner is pattern based, so findings may be incomplete or require human interpretation. <br>
Mitigation: Treat results as review guidance, verify important findings manually, and combine the output with normal code review and security checks. <br>


## Reference(s): <br>
- [GQLLint homepage](https://gqllint.pages.dev) <br>
- [GQLLint git hook documentation](https://gqllint.pages.dev/docs/hooks) <br>
- [ClawHub gqllint release page](https://clawhub.ai/suhteevah/gqllint) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, HTML, shell commands, configuration] <br>
**Output Format:** [Terminal text, JSON, HTML, and Markdown reports with shell command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally against selected files or directories; paid tiers unlock additional GraphQL pattern categories.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
