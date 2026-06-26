## Description: <br>
Systematically verifies academic references against scholarly databases and resolvers to help detect AI-hallucinated, fabricated, uncertain, or broken citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benchen4395](https://clawhub.ai/user/benchen4395) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, editors, reviewers, and developers use this skill to verify whether cited papers, DOI links, arXiv records, and bibliography entries genuinely exist before relying on a manuscript or generated reference list. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided papers, citation lists, or Overleaf-accessible content may contain private or unpublished research material. <br>
Mitigation: Review the material before using the skill and avoid submitting confidential manuscripts or references to agents or external services unless that sharing is approved. <br>
Risk: Verification searches may disclose citation metadata to third-party scholarly services. <br>
Mitigation: Use only approved academic search services for sensitive work, and avoid querying sensitive citation metadata where policy or confidentiality obligations prohibit disclosure. <br>
Risk: A citation may be misclassified when databases are incomplete, inaccessible, rate-limited, or return partial matches. <br>
Mitigation: Treat uncertain and not-found results as review prompts, and confirm high-impact decisions with authoritative sources such as DOI records, publisher pages, arXiv records, or library databases. <br>


## Reference(s): <br>
- [Citation Extraction and Parsing Rules](references/citation-extraction.md) <br>
- [Database Query Strategies](references/search-strategies.md) <br>
- [Authenticity Judgment Criteria](references/verification-criteria.md) <br>
- [Reference Extraction Decision Tree](scripts/extract_references.md) <br>
- [ClawHub skill page](https://clawhub.ai/benchen4395/paper-reference-checker) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown report with citation status labels and verification notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include verified, uncertain, not found, fabricated, or broken citation classifications.] <br>

## Skill Version(s): <br>
1.2.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
