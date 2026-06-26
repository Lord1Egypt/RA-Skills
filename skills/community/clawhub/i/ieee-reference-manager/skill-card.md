## Description: <br>
Helps agents review and repair IEEE-style LaTeX and BibTeX references, including citation consistency, required fields, journal macro normalization, DOI metadata checks, Early Access handling, author-count rules, and duplicate detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZLHad](https://clawhub.ai/user/ZLHad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, authors, and technical editors use this skill to audit IEEE paper references, repair BibTeX entries, check citation coverage across .tex and .bib files, normalize IEEE journal names, and prepare user-reviewed bibliography edits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Online DOI validation can disclose draft titles, authors, or DOI values to external services. <br>
Mitigation: Avoid web-based DOI validation for confidential drafts unless sharing that metadata externally is acceptable. <br>
Risk: Automated bibliography or citation edits can introduce incorrect references or formatting changes. <br>
Mitigation: Review proposed diffs and Before/After examples before accepting edits. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/ZLHad/ieee-reference-manager) <br>
- [IEEE Reference Guide](https://journals.ieeeauthorcenter.ieee.org/wp-content/uploads/sites/7/IEEE_Reference_Guide.pdf) <br>
- [IEEEtran BibTeX HOWTO](https://www.michaelshell.org/tex/ieeetran/bibtex/) <br>
- [IEEE reference rules](references/ieee-reference-rules.md) <br>
- [Utility script guidance](references/utility-scripts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, code blocks, and BibTeX or LaTeX snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed file edits, local analysis commands, and DOI lookup guidance for user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
