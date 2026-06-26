## Description: <br>
Converts user-provided PDF papers from a URL or local file into bilingual Markdown by extracting text, preserving images, and adding paragraph-by-paragraph Chinese translation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caottt](https://clawhub.ai/user/caottt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and researchers use this skill to turn academic PDFs into side-by-side bilingual Markdown for reading, study, and translation comparison. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF URLs, extracted paper text, and generated bilingual Markdown may contain confidential, regulated, unpublished, or otherwise sensitive content. <br>
Mitigation: Use only documents that are approved for the active LLM session and local storage policy. <br>
Risk: Remote PDF download and local PDF processing may handle untrusted files. <br>
Mitigation: Download from trusted sources, review the file before processing, and keep PDF tooling updated. <br>
Risk: LLM translation can omit, mistranslate, or overstate technical meaning. <br>
Mitigation: Review generated translations against the original text before relying on them for research or publication decisions. <br>


## Reference(s): <br>
- [Paper Bilingual release page](https://clawhub.ai/caottt/paper-bilingual) <br>
- [caottt publisher profile](https://clawhub.ai/user/caottt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Bilingual Markdown with extracted figure assets and supporting Python or PowerShell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves one paper per folder under memory/paper-bilingual with index.md and figure assets.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
