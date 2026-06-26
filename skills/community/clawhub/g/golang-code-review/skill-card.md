## Description: <br>
Reviews Go source files for formatting, quality, error-handling, and maintainability issues, then produces a structured review report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[knifeAn](https://clawhub.ai/user/knifeAn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review Go code before or during merge workflows, focusing on formatting, static-analysis signals, error handling, best-practice checks, and concise remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can suggest commands that modify local files, such as gofmt -w. <br>
Mitigation: Run formatting commands intentionally and review source-control diffs before committing changes. <br>
Risk: The security evidence describes this as a lightweight local review aid rather than a complete security audit. <br>
Mitigation: Use it as a supplemental review signal and keep dedicated security review, testing, and static-analysis gates for higher-risk code. <br>
Risk: External Go analysis tools may change behavior when installed at latest versions. <br>
Mitigation: Pin tool versions in controlled or reproducible environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/knifeAn/golang-code-review) <br>
- [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments) <br>
- [Go Error Handling Best Practices](https://github.com/golang/go/wiki/ErrorHandlingBestPractices) <br>
- [Effective Go](https://golang.org/doc/effective_go.html) <br>
- [Staticcheck](https://staticcheck.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style review report with issue counts, severity labels, line references, metrics, remediation guidance, and optional shell commands for Go tooling.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May suggest local formatting and analysis commands such as gofmt, goimports, go vet, staticcheck, errcheck, and golint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
