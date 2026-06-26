## Description: <br>
Comprehensive documentation guide for Golang projects, covering godoc comments, README, CONTRIBUTING, CHANGELOG, Go Playground, Example tests, API docs, and llms.txt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to write or review Go documentation across libraries, CLIs, and services. It guides agents through doc comments, README, CONTRIBUTING, CHANGELOG, API documentation, Go examples, and AI-friendly documentation files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated documentation can introduce inaccurate API behavior, misleading obligations, or unsupported rationale. <br>
Mitigation: Review generated documentation against the code and preserve documented constraints, warnings, and required actions before publishing. <br>
Risk: The skill suggests optional use of public documentation services such as Go Playground, pkg.go.dev, Context7, DeepWiki, OpenDeep, and zRead. <br>
Mitigation: Do not submit private code or internal documentation to public services unless that disclosure is intended and approved. <br>
Risk: The skill can run Go, lint, git, web fetch, and file editing actions through the host agent. <br>
Mitigation: Review proposed commands and file edits before applying them in sensitive repositories. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/samber/golang-documentation) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/samber) <br>
- [Project Homepage](https://github.com/samber/cc-skills-golang) <br>
- [Application Documentation](artifact/references/application.md) <br>
- [Code Comments](artifact/references/code-comments.md) <br>
- [Library Documentation](artifact/references/library.md) <br>
- [Project Documentation](artifact/references/project-docs.md) <br>
- [pkg.go.dev](https://pkg.go.dev) <br>
- [Go Playground](https://go.dev/play/) <br>
- [Keep a Changelog](https://keepachangelog.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Go code blocks, shell commands, and file-edit guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or edit documentation files, Go examples, README content, CONTRIBUTING content, CHANGELOG entries, API docs, and llms.txt content.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
