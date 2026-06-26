## Description: <br>
Discovers and downloads static PDF files from Investor Relations sites, including annual reports and quarterly result PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangwllu](https://clawhub.ai/user/wangwllu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to discover candidate public IR PDF URLs from company domains, Wayback, or SEC EDGAR, then download verified PDF documents for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts public web sources and may download files from user-supplied or discovered URLs. <br>
Mitigation: Use explicit trusted IR, SEC, or Wayback targets and review domains before running downloads. <br>
Risk: Discovered links or issuer aliases can point to the wrong company, year, or archived document. <br>
Mitigation: Double-check issuer matches, source, year, and downloaded PDF content before relying on the document. <br>
Risk: Downloaded PDFs are saved into the workspace. <br>
Mitigation: Choose output directories intentionally and inspect downloaded files before sharing or using them downstream. <br>


## Reference(s): <br>
- [Issuer hints](references/issuers.json) <br>
- [ClawHub skill page](https://clawhub.ai/wangwllu/ir-pdf-downloader) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; CLI text or JSON results; downloaded PDF files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May contact public IR, SEC, and Wayback sources; downloaded PDFs are saved under downloads/ or a requested output directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
