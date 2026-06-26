## Description: <br>
Literature Daily Report collects recent PubMed, bioRxiv, and arXiv publications in life sciences and AI, filters them by topic, and generates Chinese-language daily literature reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biociao](https://clawhub.ai/user/biociao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, lab staff, and agents use this skill to track new life sciences and AI publications, categorize them, and produce a daily Chinese Markdown report with summaries and recommendations. It can also support local report organization and optional Zotero, ClawLib, and Matrix publishing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated literature reports may be copied to ClawLib, sent to Matrix, and added to a Zotero group library. <br>
Mitigation: Review the script before installation and disable or remove shared-service publishing steps when local-only report generation is required. <br>
Risk: Zotero integration uses a group library and API key, which can affect shared library contents. <br>
Mitigation: Use a limited-scope Zotero API key, verify the intended group ID, and inspect the Zotero helper workflow before enabling it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/biociao/literature-daily-report) <br>
- [Publisher profile](https://clawhub.ai/user/biociao) <br>
- [Category reference](references/categories.md) <br>
- [Workflow reference](references/workflows.md) <br>
- [Zotero API key setup](https://www.zotero.org/settings/keys/new) <br>
- [bioRxiv API endpoint](https://api.biorxiv.org/details/biorxiv/{date_from}/{date_to}/0/json) <br>
- [arXiv export API endpoint](http://export.arxiv.org/api/query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese Markdown literature reports with setup and execution guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are saved as dated Markdown files and latest.md; optional workflows can copy reports to ClawLib, add items to a Zotero group library, and send reports to Matrix.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
