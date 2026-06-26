## Description: <br>
Repairs malformed JSON files by normalizing loose JSON-like content through Node.js evaluation for cases such as trailing commas, single quotes, unquoted keys, comments, and non-decimal numbers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanng-ide](https://clawhub.ai/user/wanng-ide) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and operators use this skill to repair malformed local JSON files or directories by converting common JSON-like syntax into valid formatted JSON. It is best suited for trusted configuration or manually edited data files where users can review the resulting diff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Malformed files are treated as JavaScript during repair, which can run unexpected code. <br>
Mitigation: Use only on trusted local files and prefer a JSON5 or JSON repair tool that parses without executing input for untrusted content. <br>
Risk: The skill can rewrite local files, especially when scanning directories recursively. <br>
Mitigation: Keep backups enabled, avoid recursive mode on downloaded or large project trees, and review diffs before relying on repaired output. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wanng-ide/json-repair-kit) <br>


## Skill Output: <br>
**Output Type(s):** [files, json, shell commands, guidance] <br>
**Output Format:** [JSON files with terminal status messages and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates .bak backups by default for in-place repairs.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
