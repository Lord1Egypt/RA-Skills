## Description:

Searches and synthesizes biomedical literature through PubMed for clinical studies, drug information, treatment guidelines, and biomedical research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anightmare2](https://clawhub.ai/user/anightmare2)

### License/Terms of Use:

MIT-0

## Use Case:

Clinicians, researchers, and agents supporting biomedical workflows use this skill to search PubMed, retrieve relevant papers, and frame findings by common evidence-quality categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented PubMed curl command can become unsafe if an untrusted query is inserted directly into a shell command string.

Mitigation: Use a structured HTTP client or curl with --get and --data-urlencode for the search term, and avoid placing user-provided queries directly inside shell command strings.

Risk: Biomedical search summaries can be mistaken for clinical advice or overstate the quality of retrieved evidence.

Mitigation: Treat outputs as literature-retrieval assistance, verify cited studies and evidence categories, and route clinical decisions through qualified medical review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anightmare2/skills/medical-lit)
- [NCBI PubMed E-utilities API](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with PubMed search queries and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results and summaries should be reviewed for medical accuracy and source quality before use.]

## Skill Version(s):

0.1.0 (source: server release evidence, clawhub.yaml, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
