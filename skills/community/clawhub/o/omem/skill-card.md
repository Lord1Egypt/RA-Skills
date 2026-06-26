## Description: <br>
Searches a user's local OMem work-memory index across emails, calendar events, documents, and collaboration notes to help answer work-context questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seacen](https://clawhub.ai/user/seacen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and their agents use this skill to search local work history, decisions, meetings, documents, and colleagues, then fetch the most relevant OMem wiki pages or raw parsed artifacts when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can query sensitive local work memory, including emails, calendar items, documents, and notes. <br>
Mitigation: Install and use it only when the user wants agent access to that OMem index; scope ambiguous requests with account, source, date range, or document type when needed. <br>
Risk: Search ranking may return plausible but irrelevant pages when a query is broad or ambiguous. <br>
Mitigation: Read returned abstracts, rerank before opening pages, and cite OMem source paths so the user can verify the answer. <br>


## Reference(s): <br>
- [OMem documentation](https://seacen.github.io/omem/) <br>
- [OMem install script](https://github.com/seacen/omem/releases/latest/download/install.sh) <br>
- [Query syntax and edge cases](references/query-syntax.md) <br>
- [CLI output schemas](references/output-schemas.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain text with cited OMem source paths and occasional inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON parsing of OMem CLI results and source-path citations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
