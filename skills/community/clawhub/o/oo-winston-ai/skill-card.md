## Description:

Checks text or public URLs for plagiarism, AI-generation, similarity, and fact-checking signals using Winston AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this integration to assess submitted text or public URLs for plagiarism, likely AI-generated content, similarity between texts, and factual claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions run an installer whose remote contents and downloaded CLI were not verified.

Mitigation: Review and verify the CLI installation separately, including its effects on other agents' skills, before allowing automatic setup.

Risk: Text or URLs submitted for analysis may incur credit usage or be processed by OOMOL and Winston AI.

Mitigation: Submit only content intended for those services and establish acceptable credit usage first.

## Reference(s):

- [Winston AI](https://gowinston.ai)
- [Winston AI API documentation](https://docs.gowinston.ai/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON results with text-based analysis findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may report plagiarism, AI-detection, text-similarity, or fact-checking signals.]

## Skill Version(s):

1.0.4 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
