## Description: <br>
Searches, retrieves, and summarizes content from Our World in Data using the `owid-catalog` Python module. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rachmann-alexander](https://clawhub.ai/user/rachmann-alexander) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to search OWID charts, fetch chart metadata and data, and return concise, attributed summaries for user questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill adds the pinned `owid-catalog` Python package and depends on access to OWID's public service. <br>
Mitigation: Review the dependency under normal Python package controls and allow outbound OWID access only where appropriate. <br>
Risk: OWID searches can return ambiguous results, and concise summaries may omit important nuance. <br>
Mitigation: Use precise queries, limit candidate results, validate the selected chart against the user's question, and include the source URL for attribution. <br>


## Reference(s): <br>
- [owid-catalog Python package](https://pypi.org/project/owid-catalog/) <br>
- [ClawHub skill page](https://clawhub.ai/rachmann-alexander/owid-oc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Structured text or JSON-like objects containing chart title, description, URL, and data summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Searches should be performed in English; translated answers should preserve factual meaning and include attribution to OWID.] <br>

## Skill Version(s): <br>
0.1.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
