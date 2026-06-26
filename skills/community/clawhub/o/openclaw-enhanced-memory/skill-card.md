## Description: <br>
Enhanced Memory provides OpenClaw agents with structured, searchable, long-lived local memory using categorized directories, inline tags, lifecycle archiving, and query-based retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fatcatMaoFei](https://clawhub.ai/user/fatcatMaoFei) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to organize agent memory into durable Markdown files, search memory with tags, route retrieval by query type, and archive older entries without deleting them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed for long-lived local memory, so personal notes can persist in active or archived files. <br>
Mitigation: Avoid storing secrets or highly sensitive personal information, review the memory directory periodically, and install the skill only when persistent local memory is desired. <br>
Risk: The lifecycle manager moves older memory files into an archive, which can affect active-memory availability if run unexpectedly or with a low threshold. <br>
Mitigation: Keep backups before running lifecycle management and review the archive threshold before scheduled or manual runs. <br>
Risk: Search examples accept user-provided query strings, which can be mishandled if another tool wraps them in shell commands unsafely. <br>
Mitigation: Pass search queries as safe command arguments instead of constructing shell commands through raw string concatenation. <br>


## Reference(s): <br>
- [Tagged Memory Architecture Reference](artifact/references/architecture.md) <br>
- [ClawHub release page](https://clawhub.ai/fatcatMaoFei/openclaw-enhanced-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and Python script behavior] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Markdown files and Python standard-library scripts; no external service or API-key dependency is described.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
