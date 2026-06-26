## Description: <br>
Analyze HTML document structure and content with MinerU, returning structured Markdown with layout, headings, and content hierarchy preserved. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SEO analysts, and content auditors use this skill to inspect local or remote HTML, understand document structure, and preserve extracted layout information as Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on the third-party MinerU service and mineru-open-api package. <br>
Mitigation: Install and use it only when MinerU and the package source are trusted for the target environment. <br>
Risk: MINERU_TOKEN is required for HTML extraction and could grant service access if exposed. <br>
Mitigation: Store the token as a protected secret or environment variable and avoid committing it, sharing it, or writing it to logs. <br>
Risk: Submitted HTML, internal URLs, or crawled page content may contain confidential or regulated information. <br>
Mitigation: Use the skill only when MinerU's data handling is acceptable for the material being analyzed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mzlzyca/html-analysis) <br>
- [MinerU homepage](https://mineru.net) <br>
- [MinerU repository](https://github.com/opendatalab/MinerU) <br>
- [MinerU API token management](https://mineru.net/apiManage/token) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and MinerU CLI usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses mineru-open-api with MINERU_TOKEN; document content is written to stdout by default and progress messages to stderr.] <br>

## Skill Version(s): <br>
0.4.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
