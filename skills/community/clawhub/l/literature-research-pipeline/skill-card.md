## Description: <br>
端到端学术文献检索与下载全流程自动化，支持检索、推荐、多渠道下载、Ablesci 求助监控、通知和进度追踪。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oreosofat](https://clawhub.ai/user/oreosofat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and technical users use this skill to search academic literature, select high-value papers, attempt permitted downloads, and track fulfillment through direct sources or Ablesci help requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reuse a logged-in browser session to post Ablesci help requests and download files. <br>
Mitigation: Use a dedicated browser profile for Ablesci and require explicit user confirmation before posting or downloading. <br>
Risk: The skill can create recurring monitoring jobs. <br>
Mitigation: Require confirmation before creating cron jobs and remove the recurring monitor when the task is finished. <br>
Risk: Downloaded papers and progress files may contain private research interests or document metadata. <br>
Mitigation: Keep download and progress paths private and avoid shared directories unless intentionally configured. <br>
Risk: The workflow depends on a separate literature-search skill executed through subprocess calls. <br>
Mitigation: Verify the dependent literature-search skill before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oreosofat/literature-research-pipeline) <br>
- [Unpaywall API endpoint](https://api.unpaywall.org/v2/{DOI}?email={LIT_UNPAYWALL_EMAIL}) <br>
- [DOI resolver](https://doi.org/{DOI}) <br>
- [Semantic Scholar PDF endpoint](https://api.semanticscholar.org/graph/v1/paper/{DOI}/PDF) <br>
- [Crossref works endpoint](https://api.crossref.org/works/{DOI}) <br>
- [Ablesci assist create](https://www.ablesci.com/assist/create) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API calls, Files, Configuration guidance] <br>
**Output Format:** [Markdown with inline code blocks, API endpoints, progress tables, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write downloaded PDFs and a literature progress file when configured by the user.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and CHANGELOG.md, released 2026-04-14) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
