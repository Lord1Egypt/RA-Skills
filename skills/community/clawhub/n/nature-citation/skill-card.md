## Description:

Strict Nature/CNS-family citation retrieval, verification, and export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1bai](https://clawhub.ai/user/yang1bai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, researchers, and manuscript authors use this skill to find supporting citations, verify DOI and retraction status, and export reference lists for Nature-series manuscripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Citation queries may contain unpublished research, confidential manuscript text, proprietary project names, or private reference lists.

Mitigation: Use the skill only for non-sensitive topics unless a reviewer approves external lookup and redacts sensitive query terms first.

Risk: The workflow sends user research queries to a fixed third-party personal-library endpoint before broader citation lookup.

Mitigation: Require explicit user consent before using the personal-library search, or skip that endpoint when ownership, retention, or access controls are unclear.

Risk: Citation retrieval can return papers that are related but do not actually support the user claim.

Mitigation: Review each candidate citation for claim support, DOI accuracy, metadata consistency, and retraction or correction status before using it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yang1bai/skills/nature-citation)
- [CrossRef Works API query](https://api.crossref.org/works?query=<query>)
- [CrossRef Works API DOI lookup](https://api.crossref.org/works/<DOI>)
- [Personal LitReview library search](https://ybliterature.com/api/search?q=<URL-encoded-query>)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown reference lists with optional BibTeX, RIS, ENW, or Zotero RDF export blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes support assessment, DOI verification status, citation counts, and retraction-check notes when available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
