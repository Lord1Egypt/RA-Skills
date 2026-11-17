## Description:

Turns a user-provided Obsidian note or Markdown outline into a KMind mind map PNG by default, with editable KMind or SVG output only on request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suka233](https://clawhub.ai/user/suka233)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert pasted Markdown, an Obsidian note, or one explicitly named note file into a KMind mind map while keeping vault access limited to the provided content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A first-time run may install and use the named core renderer skill, which will process the provided note content.

Mitigation: Require explicit approval before installing the exact core skill and use it only for notes the user is comfortable processing with that dependency.

Risk: Broad vault access or note mutation could expose unrelated Obsidian content.

Mitigation: Process only pasted content or one explicitly provided note path, and do not scan the vault, read global Obsidian configuration, rewrite notes, move notes, rename notes, or delete notes.

Risk: The delegated renderer may report missing runtime requirements.

Mitigation: Surface missing Node.js or browser requirements clearly instead of bypassing them or substituting a different installer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/suka233/skills/obsidian-note-to-mindmap)
- [Audited core skill](https://clawhub.ai/suka233/kmind-markdown-to-mindmap)
- [KMind Zen](https://kmind.app)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PNG by default; editable .kmindz.svg or SVG only when explicitly requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask for confirmation before installing the exact audited core skill through the ClawHub CLI.]

## Skill Version(s):

0.1.0 (source: frontmatter, package.json, CHANGELOG, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
