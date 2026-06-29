## Description: <br>
Searches academic literature via arXiv, Semantic Scholar, and open-access PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to find academic papers, citations, formal research, and open-access paper versions for literature reviews or citation chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad triggers such as "pdf" and "papers" may activate the skill for requests that are not academic literature searches. <br>
Mitigation: Use or install the skill when requests clearly involve scholarly paper discovery, citation lookup, literature reviews, or PDF-based research extraction. <br>
Risk: Fallback PDF extraction may preserve tables and figures less cleanly than the preferred document-conversion path. <br>
Mitigation: Prefer the configured document-conversion capability for PDFs and note extraction limits when using fallback page reads. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/athola/skills/nm-tome-papers) <br>
- [Tome Plugin Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/tome) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include paper metadata, citation chains, PDF extraction notes, and open-access fallback guidance.] <br>

## Skill Version(s): <br>
1.9.13 (source: ClawHub release metadata; artifact frontmatter says 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
