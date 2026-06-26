## Description: <br>
Searches academic literature via arXiv, Semantic Scholar, and open-access PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, students, and developers use this skill to find academic papers, build literature reviews, trace citation chains, and extract key findings from open-access papers and PDFs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Confidential PDFs, private file paths, or URLs containing access tokens may be exposed to document-conversion tooling during paper extraction. <br>
Mitigation: Review PDF sources and URLs before conversion, avoid passing secrets or private documents unless the configured conversion tool is approved for that data, and prefer sanitized public links when possible. <br>
Risk: Academic search results, paper availability, and extracted paper content can be incomplete or misleading. <br>
Mitigation: Cross-check important claims against the original paper and authoritative citation sources before using the results in decisions or published work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-tome-papers) <br>
- [Tome plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/tome) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, API Calls] <br>
**Output Format:** [Markdown with research summaries, citation details, and PDF extraction notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference arXiv, Semantic Scholar, Unpaywall, CORE.ac.uk, PubMed Central, author preprint pages, and document-conversion tooling when available.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence; artifact frontmatter says 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
