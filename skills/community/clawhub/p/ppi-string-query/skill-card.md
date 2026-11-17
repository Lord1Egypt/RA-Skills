## Description:

Query STRING database for protein-protein interactions with confidence scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hollyya](https://clawhub.ai/user/hollyya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and bioinformatics analysts use this skill to query STRING for interaction partners by UniProt accession, inspect confidence scores, and build protein interaction networks for pathway analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The example script modifies Python import search paths, which can load unintended local code if run from an untrusted directory.

Mitigation: Run the example only from a trusted directory or virtual environment, and prefer importing open_biomed from a trusted installed package.

Risk: STRING results can include functional associations and literature-derived signals that may not prove direct physical binding.

Mitigation: Review the individual evidence channels and cross-reference critical interactions with primary databases or literature before using results for decisions.

## Reference(s):

- [STRING Score Methodology](references/score_details.md)
- [STRING API Docs](https://string-db.org/help/api/)
- [STRING Documentation](https://string-db.org/help/)

## Skill Output:

**Output Type(s):** [Guidance, Code, JSON]

**Output Format:** [Markdown guidance with Python code blocks and JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include STRING combined and channel-specific confidence scores for interaction partners.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
