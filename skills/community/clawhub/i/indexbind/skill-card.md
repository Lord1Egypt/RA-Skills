## Description:

Helps an agent install and use indexbind from Node, browsers, Web Workers, or Cloudflare Workers by choosing the right package, CLI, artifact, and entrypoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add or operate indexbind-based local search for documentation or knowledge-base content across Node, browser, Web Worker, and Cloudflare Worker environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npm install and npx examples can expose users to supply-chain changes in the indexbind package.

Mitigation: Prefer a pinned indexbind version or a project-local dependency with a lockfile, and avoid global installs unless they are required.

Risk: Indexing unintended directories can make private or irrelevant content searchable.

Mitigation: Run indexing only on directories intended for search and review index-scoped configuration before publishing artifacts or bundles.

## Reference(s):

- [Indexbind ClawHub Skill Page](https://clawhub.ai/jolestar/skills/indexbind)
- [Getting Started](https://indexbind.jolestar.workers.dev/guides/getting-started.md)
- [Packaging Reference](https://indexbind.jolestar.workers.dev/reference/packaging.md)
- [API Reference](https://indexbind.jolestar.workers.dev/reference/api.md)
- [CLI Reference](https://indexbind.jolestar.workers.dev/reference/cli.md)
- [Runtime Model](https://indexbind.jolestar.workers.dev/concepts/runtime-model.md)
- [Canonical Bundles](https://indexbind.jolestar.workers.dev/concepts/canonical-bundles.md)
- [Adoption Examples](https://indexbind.jolestar.workers.dev/guides/adoption-examples.md)
- [Web and Cloudflare Guide](https://indexbind.jolestar.workers.dev/guides/web-and-cloudflare.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
