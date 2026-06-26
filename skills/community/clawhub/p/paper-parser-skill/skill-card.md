## Description: <br>
CLI tool to search, download, and parse academic papers from arXiv into AI-friendly Markdown using MinerU API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaihangyang](https://clawhub.ai/user/kaihangyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to find arXiv papers, download PDFs, and convert selected papers into AI-friendly Markdown through the MinerU parsing service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the third-party PyPI package executes third-party code on the user's system. <br>
Mitigation: Use a virtual environment or container and confirm the intended package and version before installation. <br>
Risk: Parsing sends selected PDFs and paper metadata to MinerU for external processing. <br>
Mitigation: Submit only PDFs the user is allowed to share, avoid sensitive unpublished documents, and review MinerU's data handling terms. <br>
Risk: The MinerU API token is required for parsing and could expose account access if leaked. <br>
Mitigation: Use a dedicated revocable token and keep it protected in the local configuration file. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaihangyang/paper-parser-skill) <br>
- [PyPI package](https://pypi.org/project/paper-parser-skill/) <br>
- [MinerU parsing service](https://mineru.net/) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, markdown] <br>
**Output Format:** [Markdown with inline shell commands and YAML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents toward local workspace files and asynchronous parsing commands when cloud conversion may take several minutes.] <br>

## Skill Version(s): <br>
0.1.4 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
