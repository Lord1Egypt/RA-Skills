## Description: <br>
Organize and classify OpenClaw knowledge entries into local folders by content type (Research, Decision, Insight, Lesson, Pattern, Project, Reference, Tutorial). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ClaireAICodes](https://clawhub.ai/user/ClaireAICodes) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to turn MEMORY.md and daily memory files into a structured local knowledge base with classified markdown entries and indexes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Index generation has a code-execution bug in tag parsing. <br>
Mitigation: Review local-file behavior before installation and prefer a patched version that replaces the eval tag parser with safe parsing. <br>
Risk: Cleanup can permanently delete local files when paths or sync state are wrong. <br>
Mitigation: Use explicit --workspace and --output-dir arguments, run km sync --dry_run and km cleanup --dry_run first, and avoid scheduled cleanup until paths and state are verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ClaireAICodes/knowledge-management) <br>
- [Publisher profile](https://clawhub.ai/user/ClaireAICodes) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown files with YAML frontmatter, JSON classification output, index markdown, and CLI command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local memory files and writes organized local folders, sync state, logs, and index files.] <br>

## Skill Version(s): <br>
2.1.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
