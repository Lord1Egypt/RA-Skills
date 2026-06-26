## Description: <br>
Golang data structures: slices, maps, arrays, container/list/heap/ring, strings.Builder versus bytes.Buffer, generic collections, pointers, and copy semantics for choosing and optimizing Go data structures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to choose, implement, and optimize Go data structures while reasoning about memory layout, allocation cost, access patterns, and standard-library container tradeoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated guidance or code changes could introduce incorrect data-structure choices, unsafe pointer misuse, or performance regressions. <br>
Mitigation: Review proposed code and explanations, run Go tests and benchmarks where relevant, and apply unsafe pointer patterns only when they match the documented Go rules. <br>
Risk: The skill can suggest local Go, golangci-lint, and git commands that may affect a working tree. <br>
Mitigation: Inspect commands before execution and run them in a trusted workspace with normal source-control safeguards. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/samber/golang-data-structures) <br>
- [Project Homepage](https://github.com/samber/cc-skills-golang) <br>
- [Slice Internals Deep Dive](references/slice-internals.md) <br>
- [Map Internals Deep Dive](references/map-internals.md) <br>
- [Container Packages and String Builders](references/containers.md) <br>
- [Writing Generic Data Structures](references/generics.md) <br>
- [Pointer Types Deep Dive](references/pointers.md) <br>
- [Go Data Structures](https://research.swtch.com/godata) <br>
- [The Go Memory Model](https://go.dev/ref/mem) <br>
- [Effective Go](https://go.dev/doc/effective_go) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands] <br>
**Output Format:** [Markdown with Go code examples and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits or Go tooling commands for projects using Go.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
