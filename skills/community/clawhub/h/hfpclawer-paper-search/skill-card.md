## Description: <br>
Discover, download, and organize academic papers from arXiv, HuggingFace Papers, and OpenReview, including multi-source search, deduplication, PDF download, Markdown conversion, and optional wiki sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diamond2nv](https://clawhub.ai/user/diamond2nv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and research developers use this skill to monitor new academic papers, configure topic searches, download matching PDFs, convert them to Markdown, and optionally sync paper notes into a wiki. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the full pipeline can download papers, consume disk space, and write local files including optional wiki output. <br>
Mitigation: Install in a dedicated project or virtual environment, review config.yaml before running, and start with --dry-run or step-by-step commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diamond2nv/hfpclawer-paper-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may lead an agent to create local configuration, SQLite data, downloaded PDFs, converted Markdown, and optional wiki files through the hfpclawer CLI.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
