## Description:

Provides answers by retrieving and synthesizing information from local text or markdown files using a retrieval-augmented generation approach.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metatronsdoob369](https://clawhub.ai/user/metatronsdoob369)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to answer questions against a focused folder of local text or markdown documents and return supporting matches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and document snippets may be sent to an external OpenAI-backed workflow.

Mitigation: Keep docsPath pointed at a narrow, non-sensitive folder and avoid private, regulated, credential-containing, or broad directories unless that content is intended for model requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/metatronsdoob369/skills/hk101-living-rag)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Synthesized answer with matched document paths, scores, and snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses query, optional docsPath, and optional top-k match count; requires OPENAI_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
