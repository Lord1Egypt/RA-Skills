## Description: <br>
Filesystem librarian for OpenClaw environments that scans, catalogs, and organizes file structures by identifying orphaned files, misplaced assets, stale artifacts, broken references, and structural inefficiencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcroebuck](https://clawhub.ai/user/mcroebuck) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use Lexi to audit local filesystem structure, build a catalog of files and directories, review cleanup recommendations, and execute approved organization changes with archive safeguards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read broad local filesystem paths, parse references in file contents, and inspect scheduled-task or runtime configuration files. <br>
Mitigation: Set a narrow scan root, confirm exclusions before scanning, and exclude secrets, private projects, and other protected paths. <br>
Risk: The skill can propose file moves, deletions, and reference updates during later workflow phases. <br>
Mitigation: Require explicit user approval before each change batch, archive files before removal, and verify references after each approved batch. <br>


## Reference(s): <br>
- [Lexi Scanning Framework](scanning-framework.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, catalog entries, structured inventories, action plans, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes read-only audit phases, approval-gated file changes, archive manifests, changelogs, and filesystem catalog updates.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
