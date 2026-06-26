## Description: <br>
This skill maps construction data to standard ontologies and creates semantic mappings between different data schemas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Construction data teams, BIM specialists, and developers use this skill to map project schemas and field values to IFC, COBie, Uniclass, OmniClass, MasterFormat, UniFormat, or custom ontologies, then review mapping confidence and recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can work with project files and offer exports, so it may access or write data outside the user's intended scope if paths are not reviewed. <br>
Mitigation: Grant access only to the project files that should be mapped and review any export path before writing Excel, CSV, or JSON output. <br>
Risk: Ontology mappings may include low-confidence, uncertain, or unmapped fields that could affect downstream construction data interpretation. <br>
Mitigation: Review confidence distributions, recommendations, and unmapped fields before relying on generated mappings. <br>
Risk: The scan guidance notes a version mismatch between the artifact manifest and the registry release metadata. <br>
Mitigation: Use the server release version for this card and confirm release provenance if exact package lineage matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/datadrivenconstruction/ontology-mapper) <br>
- [Data Driven Construction homepage](https://datadrivenconstruction.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown reports, structured tables, JSON exports, and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Excel, CSV, or JSON exports; results can include mapping confidence, coverage statistics, recommendations, and custom mapping guidance.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
