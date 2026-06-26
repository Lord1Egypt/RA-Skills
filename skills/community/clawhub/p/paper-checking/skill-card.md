## Description: <br>
Paper Checking guides agents through installing and using a Windows document-plagiarism checking system for vertical and horizontal similarity checks and report review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cn-big-cabbage](https://clawhub.ai/user/cn-big-cabbage) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, educators, procurement reviewers, and internal teams use this skill to set up and operate a document similarity checker for theses, bids, project applications, and other documents, then interpret generated RTF and CSV reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive theses, bids, or internal documents may be processed by the local checker without proper authorization. <br>
Mitigation: Use the skill only with documents the user is authorized to process and keep source files, comparison libraries, reports, and recovery files in approved storage locations. <br>
Risk: Similarity scores may be misleading if thresholds, keyword filters, or preprocessing settings are inappropriate for the document type. <br>
Mitigation: Review threshold and preprocessing choices before relying on results, and interpret RTF or CSV reports alongside the documented checking rules. <br>
Risk: Generated reports and temporary recovery files may persist on disk after checking completes or is interrupted. <br>
Mitigation: Track the configured report directory and temporary recovery file locations, then retain or remove outputs according to the user's data-handling policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cn-big-cabbage/paper-checking) <br>
- [Paper Checking upstream homepage](https://github.com/tianlian0/paper_checking_system) <br>
- [Java SDK reference](https://github.com/tianlian0/duplicate-check-sample) <br>
- [Commercial edition](https://xincheck.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command snippets, configuration examples, and report-interpretation notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides local Windows executable setup, comparison-library configuration, threshold tuning, report review, and troubleshooting.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
