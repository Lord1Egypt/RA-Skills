## Description:

Convert molecules between IUPAC, SMILES, and molecular formula using PubChem as the source of truth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guox18](https://clawhub.ai/user/guox18)

### License/Terms of Use:


## Use Case:

Developers, researchers, and chemistry-focused agents use this skill to convert, normalize, and cross-check molecule names, SMILES strings, and molecular formulas against PubChem.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Molecule identifiers are sent to PubChem for lookup.

Mitigation: Avoid using the skill for confidential unpublished compounds unless that network disclosure is acceptable.

Risk: PubChem lookup can fail or return no usable record.

Mitigation: Return the documented JSON schema with empty strings rather than guessing values from memory.

Risk: Ambiguous inputs can return multiple PubChem records.

Mitigation: Use the first record consistently and cross-check externally when the exact compound identity matters.

## Reference(s):

- [PubChem PUG-REST documentation](https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest)
- [ClawHub skill page](https://clawhub.ai/guox18/skills/intern-pubchem-name-conversion)
- [Publisher profile](https://clawhub.ai/user/guox18)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON object with smiles, iupac, and formula fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses PubChem values verbatim; returns the same schema with empty strings when lookup attempts fail.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
