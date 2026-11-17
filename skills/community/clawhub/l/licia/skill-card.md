## Description:

Licia helps agents simplify JavaScript/TypeScript code by replacing hand-written utilities with documented licia functions for type checking, data manipulation, string processing, DOM operations, and related utility work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[surunzi](https://clawhub.ai/user/surunzi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to identify common JavaScript/TypeScript utility patterns and replace them with appropriate licia imports and API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad refactoring guidance may suggest licia APIs with sensitive behavior, including evalJs, filesystem write/delete helpers, rmdir, kill, open, ajax/fetch, cookies/storage, or raw HTML insertion.

Mitigation: Review generated changes carefully and require explicit user intent before accepting suggestions that execute code, alter files or processes, perform network access, touch browser storage, or insert raw HTML.

## Reference(s):

- [Licia Documentation](artifact/DOC.md)
- [ClawHub Licia Skill Page](https://clawhub.ai/surunzi/skills/licia)

## Skill Output:

**Output Type(s):** [guidance, code, markdown]

**Output Format:** [Markdown with JavaScript/TypeScript code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose licia imports and refactors based on DOC.md API references.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
