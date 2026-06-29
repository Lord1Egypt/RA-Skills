## Description: <br>
Paid Database Access helps agents search paid academic databases through a user's authenticated browser session, then deduplicate results, enrich abstracts, rank papers, and export Markdown summaries and BibTeX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lishy227](https://clawhub.ai/user/lishy227) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Researchers, students, and literature-review agents use this skill to search IEEE Xplore, Scopus, Engineering Village, and ACM Digital Library through existing institutional access, then produce ranked paper summaries and citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate inside logged-in academic database sessions and act with the user's institutional access. <br>
Mitigation: Use a dedicated browser profile limited to the target database accounts, review applicable institution and database terms, and avoid broad unattended browsing. <br>
Risk: Cookie bridging can copy browser cookies into the OpenClaw browser profile. <br>
Mitigation: Avoid cookie_bridge unless explicitly needed, and remove copied cookies or use a disposable browser profile after the task. <br>
Risk: Paper metadata and abstracts may be sent to external AI or scholarly APIs and retained in local memory caches. <br>
Mitigation: Configure AI providers deliberately, avoid sensitive research queries where inappropriate, and delete local caches when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lishy227/paid-db-access) <br>
- [README](README.md) <br>
- [Quickstart](QUICKSTART.md) <br>
- [Reference manual](REFERENCE.md) <br>
- [License](LICENSE) <br>
- [Elsevier developer portal](https://dev.elsevier.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, BibTeX, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON intermediate files, Markdown literature-review output, and BibTeX citation output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local memory caches for paper metadata and abstracts.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
