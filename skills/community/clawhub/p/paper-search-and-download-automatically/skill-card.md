## Description: <br>
Search and download related arXiv papers by topic plus date range, or from a seed paper title/id. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ppingzhang](https://clawhub.ai/user/ppingzhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, developers, and technical users use this skill to find arXiv papers by keyword, date range, or seed paper and download matching PDFs into a local workspace directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts arXiv and writes downloaded PDFs into the workspace. <br>
Mitigation: Use reasonable result limits, keep the default ./arxiv directory unless another location is intentional, and review downloaded PDFs before opening or sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ppingzhang/paper-search-and-download-automatically) <br>
- [Publisher profile](https://clawhub.ai/user/ppingzhang) <br>
- [arXiv API endpoint](https://export.arxiv.org/api/query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and locally saved PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads PDFs into a user-selected directory, defaulting to ./arxiv, and reports found, downloaded, skipped, and output path counts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
