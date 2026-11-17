## Description:

Golang data structures - slices (internals, capacity growth, preallocation, slices package), maps (internals, hash buckets, maps package), arrays, container/list/heap/ring, strings.Builder vs bytes.Buffer, generic collections, pointers (unsafe.Pointer, weak.Pointer), and copy semantics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to choose and optimize Go data structures, implement generic containers, work with standard container packages, and reason about slice, map, pointer, and copy semantics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Low-level memory guidance may lead to unsafe.Pointer or weak pointer code that is incorrect if applied mechanically.

Mitigation: Review generated low-level code carefully against the Go unsafe and weak pointer rules before merging.

Risk: Generated changes to Go data-structure choices can alter correctness, allocation behavior, or performance.

Mitigation: Run the project's normal Go tests and relevant benchmarks before accepting proposed code edits.

## Reference(s):

- [Project homepage](https://github.com/samber/cc-skills-golang)
- [Slice Internals](references/slice-internals.md)
- [Map Internals Deep Dive](references/map-internals.md)
- [Container Packages and String Builders](references/containers.md)
- [Writing Generic Data Structures](references/generics.md)
- [Pointer Types Deep Dive](references/pointers.md)
- [Go Data Structures (Russ Cox)](https://research.swtch.com/godata)
- [The Go Memory Model](https://go.dev/ref/mem)
- [Effective Go](https://go.dev/doc/effective_go)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Go code examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Go file edits, diagnostics, and data-structure selection guidance for projects with Go source files.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
