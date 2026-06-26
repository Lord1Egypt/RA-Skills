## Description: <br>
Extracts title, keyword, and abstract metadata from academic PDF files and returns structured JSON for literature management and citation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[y-egg](https://clawhub.ai/user/y-egg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and developers use this skill to parse academic PDFs and collect citation-ready metadata for literature organization, reference preparation, and analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the first part of each selected PDF to Moonshot's API using MOONSHOT_API_KEY. <br>
Mitigation: Use it only with documents approved for third-party processing, and avoid confidential, unpublished, licensed, or personal documents unless that processing is acceptable. <br>
Risk: Dependency installation instructions do not pin package versions. <br>
Mitigation: Pin and review dependencies before deployment in managed or production environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/y-egg/pdf-literature-parser) <br>
- [Moonshot API endpoint used by the artifact](https://api.moonshot.cn/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, json] <br>
**Output Format:** [JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The JSON includes title_apa, keywords, and abstract fields; read and extraction errors are also returned as JSON messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
