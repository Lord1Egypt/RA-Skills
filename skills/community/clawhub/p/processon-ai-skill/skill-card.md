## Description:

ProcessOn AI Skill helps agents create, edit, search, and export ProcessOn flowcharts, mind maps, and related diagram files from natural language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[processonai](https://clawhub.ai/user/processonai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create new ProcessOn diagrams, edit existing ProcessOn files, search account files, and export diagrams as images or PDFs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses API-key authorization and persistent credential storage.

Mitigation: Install only if you trust ProcessOn, approve only authorization links generated during your own session, and revoke or rotate the ProcessOn API key if you suspect an authorization link was opened from an untrusted source.

Risk: The skill can create, edit, search, and export files in a user's ProcessOn account.

Mitigation: Review requested actions and generated file links or exports before relying on them or sharing them outside the account.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/processonai/processon-skills/tree/main/skills/processon-ai-skill)
- [ProcessOn homepage](https://www.processon.com)
- [ClawHub skill page](https://clawhub.ai/processonai/skills/processon-ai-skill)
- [README](artifact/README.md)
- [Flowchart reference](artifact/references/flowchart.md)
- [Mind map reference](artifact/references/mindmap.md)
- [Edit reference](artifact/references/edit.md)
- [Query reference](artifact/references/query.md)
- [Export reference](artifact/references/export.md)
- [Authentication reference](artifact/references/auth.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Configuration]

**Output Format:** [Markdown with ProcessOn file links, local export paths, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify files in the user's ProcessOn account and may export PNG, SVG, or PDF files locally.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter and bundled version files report 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
