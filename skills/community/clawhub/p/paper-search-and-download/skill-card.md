## Description: <br>
Searches arXiv for papers by topic, date range, or seed paper, then downloads matching PDFs into a local output directory with structured filenames. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ppingzhang](https://clawhub.ai/user/ppingzhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, developers, and agents use this skill to collect arXiv papers for a target topic or related to a seed paper, optionally constrained by publication dates and result count. It is useful for quickly building a local paper set for literature review or follow-up analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The downloader may retry arXiv API and PDF requests without TLS certificate verification if local certificate validation fails. <br>
Mitigation: Review the script before installation, prefer a fixed version that fails closed on certificate errors, and keep downloads limited to deliberate output directories and modest result counts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ppingzhang/paper-search-and-download) <br>
- [arXiv API endpoint](https://export.arxiv.org/api/query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance plus console status text and downloaded PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads PDFs to a local directory and names files with version and update-date prefixes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
