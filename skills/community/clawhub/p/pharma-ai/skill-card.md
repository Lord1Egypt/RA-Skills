## Description:

PharmaAI helps agents perform exploratory SMILES-based toxicity prediction and virtual screening, while its ADMET and Lipinski outputs should be treated as unvalidated placeholders.

This skill is for research and development only.

## Publisher:

[xxxrobot](https://clawhub.ai/user/xxxrobot)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and technical users can use PharmaAI to prototype molecule triage workflows that score SMILES strings for hERG, hepatotoxicity, and Ames risk and sort candidate lists. Do not use the outputs for drug-safety, medical, regulatory, or compound-prioritization decisions without independent model provenance, validation, and review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release advertises pharmaceutical assessments that the inspected code does not fully compute, including hard-coded ADMET values and Lipinski pass results.

Mitigation: Treat ADMET and Lipinski outputs as placeholders until the implementation is fixed, labeled, and independently validated against documented methods.

Risk: Model provenance and validation are not established for real drug-safety or compound-prioritization decisions.

Mitigation: Require documented model sources, checksums, training and validation evidence, and domain-appropriate scientific review before operational use.

Risk: Token handling guidance in the artifact includes shell and file-based token examples that could expose ClawHub credentials.

Mitigation: Use scoped tokens, prefer ephemeral environment injection or a secrets manager, and avoid storing tokens in persistent shell history or plaintext files.

## Reference(s):

- [PharmaAI ClawHub release](https://clawhub.ai/xxxrobot/skills/pharma-ai)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON prediction objects and plain text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts individual SMILES strings or lists of SMILES strings for batch prediction and screening.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
