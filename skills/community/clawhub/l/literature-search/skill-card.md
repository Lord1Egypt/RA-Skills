## Description: <br>
Find and compile academic literature with citation lists across Google Scholar, PubMed, arXiv, IEEE, ACM, Semantic Scholar, Scopus, and Web of Science for related-work and key-paper requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpjy](https://clawhub.ai/user/jpjy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers, students, and technical writers use this skill to find, de-duplicate, triage, and format academic citations for literature reviews, related-work sections, and topic surveys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to add a generic thinking prefix before processing requests, which may alter exact prompt wording. <br>
Mitigation: Remove or ignore the prefix when exact user wording matters. <br>
Risk: Subscription literature databases may require institutional or paid access. <br>
Mitigation: Use scoped API keys, exports, or manually supplied results instead of sharing full institutional login credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpjy/literature-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown bullet list of citations, with BibTeX or CSV available when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Each citation includes authors, title, venue, year, and DOI or URL; coverage for subscription databases depends on user-provided access.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
