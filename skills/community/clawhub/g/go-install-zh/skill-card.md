## Description: <br>
Installs and configures the Go compiler on Linux for Go project builds and tests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solidexu](https://clawhub.ai/user/solidexu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install and configure Go on Linux so they can compile programs, run tests, and manage module dependencies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shell startup files can accumulate duplicate or conflicting Go PATH, GOPATH, or GOROOT entries. <br>
Mitigation: Review ~/.bashrc or ~/.profile before appending exports, and edit or remove duplicate Go-related entries when needed. <br>
Risk: Installing the wrong or untrusted archive can produce an incompatible or unsafe Go toolchain setup. <br>
Mitigation: Confirm CPU architecture with uname -m, download only from go.dev, and verify the Go checksum when appropriate. <br>


## Reference(s): <br>
- [Go Downloads](https://go.dev/dl/) <br>
- [ClawHub release page](https://clawhub.ai/solidexu/go-install-zh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with bash code blocks and tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language installation guidance for Linux amd64 and arm64 environments.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
