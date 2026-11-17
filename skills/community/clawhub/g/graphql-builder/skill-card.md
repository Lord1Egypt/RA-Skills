## Description:

Build and validate GraphQL queries, mutations, and schemas for GraphQL API work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to draft GraphQL queries and mutations, validate or format GraphQL files, inspect schemas, and run basic introspection against trusted endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell helper can pass crafted curl arguments during introspection, which could read or write local files or contact untrusted destinations.

Mitigation: Review before installation, use only trusted simple file paths and trusted HTTPS GraphQL endpoints, avoid untrusted command arguments, and update the script to quote variables, pass -- before curl URLs, and validate destinations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/graphql-builder)
- [Publisher profile](https://clawhub.ai/user/ckchzh)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands and GraphQL snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local GraphQL files and may call trusted HTTPS GraphQL endpoints when introspection is requested.]

## Skill Version(s):

3.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
