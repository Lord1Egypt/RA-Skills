## Description: <br>
Reviews pull request diffs for syntax errors, code quality issues, security vulnerabilities, and team-standard violations across JavaScript, TypeScript, Node.js, PHP, Python, CSS, and HTML. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nesquitmx](https://clawhub.ai/user/nesquitmx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to get structured pull request review comments, severity-ranked findings, and suggested fixes before code is merged. It is intended for human-controlled review workflows, not autonomous approval or merge decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated PR integration could post comments, approvals, or merge decisions with broader repository permissions than needed. <br>
Mitigation: Use narrowly scoped repository permissions and require human control over posting comments, approvals, and merges. <br>
Risk: The skill performs static review guidance and may miss runtime failures, compilation issues, test regressions, or project-specific context. <br>
Mitigation: Use it alongside tests, linters, SAST tools, and human reviewer judgment before accepting changes. <br>
Risk: Review findings can include false positives or severity choices that do not match a team's policy. <br>
Mitigation: Have reviewers confirm findings and adapt the team conventions reference to the target repository. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nesquitmx/pr-code-reviewer) <br>
- [README](README.md) <br>
- [General Review Rules](references/general.md) <br>
- [Security Review Rules](references/security.md) <br>
- [Team Conventions](references/team-conventions.md) <br>
- [JavaScript and TypeScript Rules](references/javascript-typescript.md) <br>
- [Node.js Rules](references/nodejs.md) <br>
- [PHP Rules](references/php.md) <br>
- [Python Rules](references/python.md) <br>
- [CSS and HTML Rules](references/css-html.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown review summaries and inline findings with suggested code corrections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include severity labels, file and line references when available, rationale, and a final review verdict.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
