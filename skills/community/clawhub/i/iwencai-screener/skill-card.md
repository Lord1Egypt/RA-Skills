## Description: <br>
Analyzes links, files, text, or keywords to identify focused stock-market benefit themes, query iWenCai for related stock candidates, and generate an Excel report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caobingxi](https://clawhub.ai/user/caobingxi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and market researchers use this skill to turn market news, documents, free text, or keywords into focused stock-screening directions and an Excel workbook of iWenCai results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock-related terms derived from user links, files, text, or keywords may be sent to iWenCai during searches. <br>
Mitigation: Avoid confidential documents and private investment material unless derived query terms may leave the local environment. <br>
Risk: The skill creates local Excel or CSV reports containing screening results. <br>
Mitigation: Store and share generated reports according to the user's data-handling requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caobingxi/iwencai-screener) <br>
- [Publisher profile](https://clawhub.ai/user/caobingxi) <br>
- [iWenCai](https://www.iwencai.com) <br>
- [Artifact README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files] <br>
**Output Format:** [Markdown response plus an Excel workbook, with CSV fallback behavior in the helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Organizes results by selected industry, concept, theme, or supply-chain direction, with up to five stock results per direction and returned fields preserved where available.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence, created 2026-03-12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
