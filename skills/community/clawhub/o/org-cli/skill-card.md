## Description: <br>
Task capture, scheduling, and linked knowledge in org-mode files via the `org` CLI. Query, mutate, link, and search the user's org files and org-roam database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dcprevere](https://clawhub.ai/user/dcprevere) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent manage org-mode tasks, notes, schedules, and org-roam knowledge through the `org` CLI while preserving stable IDs for follow-up actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write tools may target files beyond the declared org workspace. <br>
Mitigation: Use a dedicated org workspace, keep file targets inside the configured org directories, and review custom targets before allowing writes. <br>
Risk: The skill encourages broad persistent capture of tasks, notes, preferences, relationships, and other personal facts. <br>
Mitigation: Avoid storing highly sensitive personal facts unless persistent retention is intended, and periodically review or prune captured org and org-roam content. <br>
Risk: The skill depends on the configured `org` executable. <br>
Mitigation: Point `ORG_CLI_BIN` to a trusted org CLI binary and keep the workspace and database paths explicit with `ORG_CLI_DIR`, `ORG_CLI_ROAM_DIR`, and `ORG_CLI_DB`. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dcprevere/org-cli) <br>
- [Publisher Profile](https://clawhub.ai/user/dcprevere) <br>
- [Project Homepage](https://github.com/dcprevere/org-cli) <br>
- [GitHub Releases](https://github.com/dcprevere/org-cli/releases) <br>
- [Task Management](references/task-management.md) <br>
- [Knowledge Management](references/knowledge-management.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with inline shell commands and JSON-oriented command handling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses org CLI JSON responses and surfaces stable IDs after writes.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata, SKILL.md frontmatter, package.json, plugin manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
