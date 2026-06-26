## Description: <br>
Strict Nature/CNS-family citation retrieval, verification, and export. Given a topic, claim, or list of papers, finds real citations, verifies DOIs, checks retraction status, and exports in BibTeX, RIS, ENW, or Zotero RDF format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1bai](https://clawhub.ai/user/yang1bai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External authors, researchers, and editors use this skill to find supporting citations for scientific claims, verify DOI metadata and retraction status, and prepare Nature-style reference exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Citation searches may disclose manuscript details, unpublished ideas, proprietary topics, or private reference lists to external lookup services. <br>
Mitigation: Do not use this skill with confidential material unless external queries to the personal-library endpoint and public research providers are acceptable. <br>
Risk: Automated citation retrieval can return references that are related but do not fully support the user's claim. <br>
Mitigation: Review the verification report, DOI metadata, retraction checks, and support assessment before relying on exported references. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yang1bai/nature-citation) <br>
- [Crossref Works API](https://api.crossref.org/works) <br>
- [Retraction Watch](https://retractionwatch.com) <br>
- [arXiv](https://arxiv.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code] <br>
**Output Format:** [Markdown with verified citation lists, verification notes, and export blocks for BibTeX, RIS, ENW, or Zotero RDF.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes ranked relevance, support assessment, citation metadata, DOI verification, and retraction-check status when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
