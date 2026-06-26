## Description: <br>
Extracts text from OFD files while preserving page, template, coordinate, and optional character-level position data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuwei19820201](https://clawhub.ai/user/liuwei19820201) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, document-processing engineers, and analysts use this skill to extract text, page/template source, coordinates, and optional character-level positions from OFD invoices or documents for downstream review or structured data processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Extracted OFD content may include sensitive invoice or document text. <br>
Mitigation: Run the skill only on OFD files intended for analysis and handle optional JSON output according to the data sensitivity of the source document. <br>
Risk: Output paths selected by the user can persist extracted text and position data on disk. <br>
Mitigation: Choose the output location deliberately and restrict access to generated JSON files when documents contain confidential information. <br>


## Reference(s): <br>
- [OFD Structure Reference](references/ofd-structure.md) <br>
- [OFD Specification](http://www.ofdspec.org/) <br>
- [OFD XML Namespace](http://www.ofdspec.org/2016) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Terminal text and optional JSON file with page, text, coordinate, template, and character-position fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include character-level positions when --show-chars is used; no network output.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
