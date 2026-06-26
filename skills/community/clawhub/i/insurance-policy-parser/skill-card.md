## Description: <br>
Parses medical insurance policy documents or pasted policy text and extracts 32 structured fields into standardized JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[long1973m](https://clawhub.ai/user/long1973m) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and insurance operations teams use this skill to convert medical insurance policy documents or pasted terms into standardized JSON for review and comparison. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical insurance policy documents may contain sensitive personal or policy information. <br>
Mitigation: Provide only documents intended for analysis and handle parsed text and generated JSON as sensitive data. <br>
Risk: Extracted fields may be incomplete or incorrect when policy language is ambiguous, scanned poorly, or not explicit. <br>
Mitigation: Manually verify the generated JSON against the original policy before using it for decisions or comparisons. <br>
Risk: The skill reads local PDF, DOCX, or TXT files and depends on Python packages for parsing. <br>
Mitigation: Use trusted input files and install the declared dependencies from trusted package sources when needed. <br>


## Reference(s): <br>
- [Output Format Specification](artifact/references/output-format.md) <br>
- [Document Parsing Script](artifact/scripts/parse_document.py) <br>
- [ClawHub Release Page](https://clawhub.ai/long1973m/insurance-policy-parser) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON with optional text extraction commands and extraction guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Extracts 14 core fields and 18 enhancement fields; Level 2 enhancement fields may be null when the source policy does not state them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
