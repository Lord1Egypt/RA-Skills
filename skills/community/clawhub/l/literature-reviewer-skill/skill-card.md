## Description: <br>
Literature Reviewer Skill guides agents through an eight-phase bilingual literature review workflow that searches academic databases, deduplicates and verifies paper metadata, formats GB/T 7714-2015 citations, and produces Markdown review documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stephenlzc](https://clawhub.ai/user/stephenlzc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and academic writers use this skill to plan and run bilingual literature searches across CNKI, Web of Science, ScienceDirect, PubMed, and Google Scholar, then synthesize selected papers into a structured literature review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate searches against academic databases, including paid, institutional, or logged-in services. <br>
Mitigation: Confirm that automated searching and downloading are allowed by the database license and site terms before use. <br>
Risk: Research topics, search results, metadata, analyses, and possibly PDFs may be stored locally in session folders. <br>
Mitigation: Use an approved storage location, review generated files for sensitive content, and clean up session data when it is no longer needed. <br>
Risk: Bulk PDF download guidance may conflict with access limits or licensing terms. <br>
Mitigation: Prefer metadata-only collection unless explicit confirmation, download controls, and cleanup steps are in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stephenlzc/literature-reviewer-skill) <br>
- [CNKI guide](references/cnki-guide.md) <br>
- [Database access guide](references/database-access.md) <br>
- [GB/T 7714-2015 citation guide](references/gb-t-7714-2015.md) <br>
- [CNKI advanced search](https://kns.cnki.net/kns8/AdvSearch) <br>
- [Web of Science advanced search](https://www.webofscience.com/wos/woscc/advanced-search) <br>
- [ScienceDirect search](https://www.sciencedirect.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown review documents, JSON metadata and paper records, and structured agent guidance with code or command snippets where needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates session folders with logs, raw and deduplicated paper records, paper analyses, references, and final literature review files.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata and artifact AGENTS.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
