## Description: <br>
Query STRING database for protein-protein interactions with confidence scores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hollyya](https://clawhub.ai/user/hollyya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and bioinformatics researchers use this skill to query STRING for UniProt-based protein interaction partners, confidence scores, and small interaction-network inputs for pathway analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries may contact the public STRING service. <br>
Mitigation: Avoid submitting sensitive research identifiers when that matters to the workflow and respect STRING rate limits for batch use. <br>
Risk: The skill depends on the provided open_biomed ppi_string_request implementation. <br>
Mitigation: Install only in an environment where that implementation is trusted and review it before deployment. <br>


## Reference(s): <br>
- [STRING Score Methodology](references/score_details.md) <br>
- [STRING API Docs](https://string-db.org/help/api/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, JSON] <br>
**Output Format:** [Markdown guidance with Python snippets and JSON-shaped STRING interaction records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries STRING through open_biomed ppi_string_request with UniProt ID, species, score threshold, and result limit.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
