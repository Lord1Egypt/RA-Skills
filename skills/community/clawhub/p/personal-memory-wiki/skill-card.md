## Description:

Uses Wikmd to manage a local personal wiki for useful information, including manual browsing, review, and ongoing updates from conversations and research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[errant](https://clawhub.ai/user/errant)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to maintain a Wikmd-backed personal knowledge base. It helps agents create, read, search, update, and version Markdown wiki pages for projects, research, decisions, resources, and recurring context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist broad conversation and research context into a local wiki.

Mitigation: Use a dedicated PERSONAL_WIKI_ROOT, keep secrets and unrelated private files out of that tree, and require confirmation before writes.

Risk: The wiki can be served over HTTP and may expose local notes if bound to a network interface.

Mitigation: Keep the Wikmd host bound to 127.0.0.1 unless network access is intentional and reviewed.

Risk: Version-control commits may include unintended files or sensitive notes.

Mitigation: Inspect staged Git files before committing and commit only intended Markdown wiki content.

Risk: Installing an unpinned Wikmd package can introduce dependency drift.

Mitigation: Use pipx or a pinned Wikmd version before enabling the skill.

## Reference(s):

- [Wikmd GitHub Repository](https://github.com/Linbreux/wikmd)
- [Wikmd Documentation](https://linbreux.github.io/wikmd/)
- [Wikmd Markdown Reference](references/wikmd-formatting.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files with shell command and YAML configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PERSONAL_WIKI_ROOT and writes within the configured local wiki tree.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
