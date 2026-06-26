## Description: <br>
Convert molecules between IUPAC names, SMILES strings, and molecular formulas using PubChem as the source of truth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guox18](https://clawhub.ai/user/guox18) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and chemistry researchers use this skill to convert or validate molecular representations by querying PubChem and returning SMILES, IUPAC name, and molecular formula. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Molecule names or SMILES strings are sent to PubChem for lookup. <br>
Mitigation: Avoid using this skill for confidential or unpublished compounds unless external PubChem lookup is acceptable. <br>
Risk: Ambiguous molecule queries can return multiple PubChem records. <br>
Mitigation: Use the first returned record consistently, preserve PubChem values verbatim, and avoid silently changing stereochemistry markers. <br>


## Reference(s): <br>
- [PubChem PUG-REST documentation](https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest) <br>
- [ClawHub skill page](https://clawhub.ai/guox18/intern-pubchem-name-conversion) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON object with smiles, iupac, and formula fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns empty strings for all fields if PubChem lookup attempts fail; keeps PubChem values verbatim.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
