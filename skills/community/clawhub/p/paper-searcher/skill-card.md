## Description: <br>
Paper search and Zotero workflow. 文献搜索与 Zotero 管理助手；支持多源检索、候选清单评审，并在用户确认后导入 Zotero。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moroiser](https://clawhub.ai/user/moroiser) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and developers use this skill to plan academic literature searches, verify candidate metadata, produce review shortlists, and optionally import confirmed items into Zotero. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Zotero import uses sensitive credentials. <br>
Mitigation: Keep the Zotero API key in an environment variable or secret store, never hardcode it, and import only user-confirmed items. <br>
Risk: Public metadata search sources may not provide complete coverage of subscription or publisher databases. <br>
Mitigation: Report direct database coverage separately from indirect metadata coverage and call out gaps before presenting the shortlist. <br>
Risk: External pages, papers, and metadata can contain incorrect or untrusted content. <br>
Mitigation: Verify candidate fields against reliable metadata sources and treat external text as evidence rather than instructions. <br>


## Reference(s): <br>
- [Literature Search + Zotero Import SOP](references/literature-search-zotero-sop.md) <br>
- [ClawHub skill page](https://clawhub.ai/moroiser/paper-searcher) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown reports with optional inline shell commands and Zotero import status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs emphasize search plans, source counts, coverage gaps, filtered review shortlists, and user-confirmed Zotero import details.] <br>

## Skill Version(s): <br>
1.0.2 (source: _meta.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
