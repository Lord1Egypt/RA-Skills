## Description:

Guides coding agents in writing, reviewing, and migrating React applications using modern React 19+ patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adhhamdev](https://clawhub.ai/user/adhhamdev)

### License/Terms of Use:

MIT

## Use Case:

Developers and coding agents use this skill to write and review React components, forms, data fetching, and concurrent interfaces, or to plan migrations from older React patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested network-fetched, unpinned codemods may change local projects unexpectedly.

Mitigation: Pin package versions, use lockfile-managed local installs, run codemods on a clean branch or in a sandbox, and review all diffs before committing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/adhhamdev/skills/modern-react-guidance)
- [Server-resolved source repository](https://github.com/adhhamdev/modern-react-guidance)
- [Actions and forms](references/actions-and-forms.md)
- [React 19+ API cheat sheet](references/api-cheatsheet.md)
- [React Compiler and memoization](references/compiler-and-memo.md)
- [Concurrent user experience](references/concurrent-ux.md)
- [Effects and data fetching](references/effects-and-data.md)
- [Migration and codemods](references/migration-codemods.md)
- [React codemods](https://github.com/reactjs/react-codemod)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands]

**Output Format:** [Markdown with code examples and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations should be checked against current React documentation before adoption.]

## Skill Version(s):

0.1.0 (source: ClawHub release; artifact metadata states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
