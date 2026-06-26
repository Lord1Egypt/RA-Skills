## Description: <br>
Configure and troubleshoot golangci-lint for Go projects, including import resolution issues, type-checking problems, and local or CI configuration tuning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[irook661](https://clawhub.ai/user/irook661) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to configure golangci-lint for Go repositories, select appropriate linters, troubleshoot import and type-checking failures, and prepare local or CI lint workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installer commands can fetch and execute remote code or extract tools into system locations. <br>
Mitigation: Review install commands before use and prefer trusted package managers, pinned releases, or checksummed artifacts for Go and golangci-lint. <br>
Risk: Lint configuration guidance may reduce type-aware checks to work around CI dependency or import-resolution failures. <br>
Mitigation: Use minimal lint profiles only for constrained CI cases, keep go.mod and go.sum current, run go mod download before linting, and retain fuller local lint profiles when possible. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/irook661/go-linter-configuration) <br>
- [Go 1.21.5 Linux AMD64 Download](https://golang.org/dl/go1.21.5.linux-amd64.tar.gz) <br>
- [golangci-lint Install Script](https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with YAML and shell command code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces golangci-lint configuration examples, troubleshooting guidance, and CI workflow snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
