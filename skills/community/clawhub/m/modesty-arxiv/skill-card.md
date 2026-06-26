## Description: <br>
Search, download, and summarize academic papers from arXiv. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modestyrichards](https://clawhub.ai/user/modestyrichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, content creators, and technical practitioners use this skill to search arXiv, inspect paper details, retrieve PDF links or downloads, and maintain an optional reading list. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional MongoDB persistence can store saved papers and reading status that may reveal research interests. <br>
Mitigation: Leave MongoDB environment variables unset for read-only use, or configure a limited-purpose database with appropriate access controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/modestyrichards/modesty-arxiv) <br>
- [Complete setup guide](https://skillboss.co/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, files, guidance] <br>
**Output Format:** [Markdown or plain text responses, optional JSON command output, and downloaded PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can optionally persist saved-paper metadata and reading status in MongoDB when configured by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
