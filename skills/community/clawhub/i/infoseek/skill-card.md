## Description: <br>
InfoSeek performs comprehensive web research on persons, organizations, or products across multiple search engines, deduplicates URLs, extracts clean content, and archives results with metadata in organized local folders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[expeditionhub](https://clawhub.ai/user/expeditionhub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and research teams use InfoSeek for background research, due diligence, media monitoring, competitive intelligence, and building local information archives about specific subjects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search subjects, context, URLs, and page requests may be sent to external search and browser providers. <br>
Mitigation: Use the skill only when external-provider sharing is acceptable, avoid person-focused dossiers without a lawful and appropriate basis, and review dependent search/browser skills separately. <br>
Risk: Local archives may contain sensitive research results and metadata. <br>
Mitigation: Keep archives in a controlled workspace, choose storage paths deliberately, and apply retention and access controls appropriate to the subject matter. <br>
Risk: The Windows deletion helper is flagged as risky due to PowerShell path handling. <br>
Mitigation: Avoid the Windows delete helper until its path handling is fixed; use a reviewed manual recycle-bin workflow when deletion is needed. <br>


## Reference(s): <br>
- [ClawHub InfoSeek Skill Page](https://clawhub.ai/expeditionhub/infoseek) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/expeditionhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, plain text, CSV, XLSX, HTML, DOCX, SQLite records, and terminal task summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Archives include source URL, website, source, publish date, title, author, editor, archived timestamp, and search task metadata.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md Version History) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
