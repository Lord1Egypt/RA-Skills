## Description:

Start an ad-hoc HTTP static file server in the current directory using one-line commands across 25+ languages and tools. Auto-detects available runtimes and recommends the best option.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flowerwrong](https://clawhub.ai/user/flowerwrong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to quickly preview static sites, share files over a local network, or test frontend assets by selecting an available local runtime and producing the corresponding one-line server command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Static server commands can expose files from the served directory, especially when bound to all interfaces.

Mitigation: Run from a dedicated non-sensitive directory and prefer localhost bindings such as 127.0.0.1 unless LAN access is explicitly needed.

Risk: Some examples can run mutable third-party code or inline server snippets.

Mitigation: Review commands before execution, avoid inline Node.js and Java examples when possible, and pin or preinstall third-party tools before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flowerwrong/skills/http-static-server)
- [Big list of HTTP static server one-liners](https://gist.github.com/willurd/5720255)
- [Python HTTP Static Server](references/python.md)
- [Node.js HTTP Static Server](references/nodejs.md)
- [Deno HTTP Static Server](references/deno.md)
- [PHP HTTP Static Server](references/php.md)
- [Ruby HTTP Static Server](references/ruby.md)
- [Go HTTP Static Server](references/go.md)
- [Rust HTTP Static Server](references/rust.md)
- [Java HTTP Static Server](references/java.md)
- [Docker HTTP Static Server](references/docker.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands depend on the installed local runtimes, selected port, bind address, and directory.]

## Skill Version(s):

2026.3.10 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
