## Description: <br>
Splits long academic or technical documents into chapters, generates structured JSON summaries, and creates a master index for retrieval and analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MRchenkuan](https://clawhub.ai/user/MRchenkuan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and researchers use this skill to turn long PDFs, Markdown files, or text documents into chapter files, JSON summaries, and a master index for overview and chapter-level analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled scripts use hard-coded local paths instead of explicit user-selected input and output locations. <br>
Mitigation: Review and modify scripts before execution so they accept explicit paths, stay within a user-approved workspace, and check before overwriting files. <br>
Risk: Generated chapters, summaries, and indexes may retain sensitive source document content. <br>
Mitigation: Process only documents approved for the target environment and disclose that generated artifacts may contain copied or summarized sensitive content. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/MRchenkuan/large-document-reader) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/MRchenkuan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance plus generated Markdown chapter files, JSON summary files, and a Markdown master index.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files may contain source document content and should be written only to a user-approved workspace.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
