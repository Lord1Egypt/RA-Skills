## Description:

Note Skill generates handwritten notebook-style single-file HTML study notes from technical content, vulnerability analysis, and knowledge summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unclecheng-li](https://clawhub.ai/user/unclecheng-li)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security practitioners, educators, and knowledge workers use this skill to turn technical material into visually styled HTML study notes with notebook or journal layouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable examples may spread exploit-oriented or privilege-escalation commands without clear safety boundaries.

Mitigation: Review generated notes before use or publication, remove unsafe commands when they are not necessary, and frame security examples as defensive analysis.

Risk: Generated HTML may contact third-party CDNs when opened even though the skill describes local single-file output.

Mitigation: Review the templates before installing or sharing output, and replace remote icon-font dependencies with local assets when offline operation or privacy is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unclecheng-li/skills/note-skill)
- [Checklist reference](artifact/references/checklist.md)
- [Components reference](artifact/references/components.md)
- [Notebook layouts reference](artifact/references/layouts.md)
- [Journal layouts reference](artifact/references/layouts-journal.md)
- [Lucide icon font](https://unpkg.com/lucide-static@latest/font/lucide.min.css)
- [Remix Icon font](https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with HTML, CSS, and JavaScript snippets for single-file HTML notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated notes are intended to open locally in a browser; bundled templates may contact third-party CDNs for icon fonts.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
