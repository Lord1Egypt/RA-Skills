## Description: <br>
Turn a user-provided Obsidian note or Markdown outline into a KMind mind map PNG by default, and an editable KMind map on request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suka233](https://clawhub.ai/user/suka233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert pasted Obsidian notes, Markdown outlines, or one explicitly provided note path into a KMind mind map. It is a wrapper that delegates rendering to the audited core skill after explicit confirmation if installation is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The wrapper may need to install the audited core KMind skill before rendering a mind map. <br>
Mitigation: Ask for explicit user confirmation and install only suka233/kmind-markdown-to-mindmap with the standard ClawHub install flow. <br>
Risk: Unexpected vault scanning or note mutation could expose or alter unrelated Obsidian content. <br>
Mitigation: Operate only on pasted content or one explicitly provided note path, and do not scan the vault or rewrite, move, rename, or delete notes. <br>
Risk: The security guidance flags sensitive maintainer-style automation as requiring review before full-access use. <br>
Mitigation: Review the skill before use in full-access environments and require explicit confirmation for moderation, publishing, or production-affecting actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/suka233/obsidian-note-to-mindmap) <br>
- [Audited Core Skill](https://clawhub.ai/suka233/kmind-markdown-to-mindmap) <br>
- [KMind Zen](https://kmind.app) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with optional shell command and generated mind map file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to PNG; produces editable .kmindz.svg or SVG only when explicitly requested.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter, package.json, CHANGELOG, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
