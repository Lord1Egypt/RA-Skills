## Description: <br>
Long Memory persistently archives full AI-agent conversations and helps retrieve prior sessions with keyword, TF-IDF, semantic, SQLite, and reporting tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zyuanjia](https://clawhub.ai/user/zyuanjia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill when they need durable cross-session memory: capturing full conversations, searching prior context, generating summaries, exporting memory, and producing local reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently captures full conversations, which may include personal, business, credential, medical, legal, or regulated information. <br>
Mitigation: Use a protected memory directory, review retention settings before use, and avoid capturing sensitive or regulated content unless local handling requirements are satisfied. <br>
Risk: Exports, HTML reports, operation logs, API responses, and git backups can expose stored conversation history. <br>
Mitigation: Treat these outputs as sensitive, restrict file and backup access, and do not expose the local API without additional access controls. <br>
Risk: The security evidence warns not to rely on the advertised encryption for strong protection. <br>
Mitigation: Use external storage encryption and established secret-management controls for high-sensitivity memory data. <br>
Risk: Importing untrusted JSON or memory files can introduce unwanted or misleading stored context. <br>
Mitigation: Import only trusted files and review imported content before using it to guide future agent behavior. <br>


## Reference(s): <br>
- [Long Memory ClawHub Release](https://clawhub.ai/zyuanjia/long-memory) <br>
- [README](README.md) <br>
- [Skill Definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown memory records, JSON CLI/API responses, plain text summaries, configuration files, and HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists archives, indexes, exports, reports, logs, backups, and API responses in a local memory directory.] <br>

## Skill Version(s): <br>
7.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
