## Description: <br>
A data desensitization skill that masks phone numbers, ID cards, bank cards, emails, IP addresses, Chinese names, path usernames, long digit sequences, and sensitive field names. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bianchengyy](https://clawhub.ai/user/bianchengyy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operations staff, and data handlers use this skill to mask sensitive values in text, logs, files, and documents before sharing data, preparing test data, or processing documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create reversible mappings that expose original sensitive values if stored, committed, backed up, or shared. <br>
Mitigation: Use restoration only when needed and protect generated mapping files like secrets; keep them out of commits, shared workspaces, and backups. <br>
Risk: Regex-based masking may miss sensitive values outside the documented rules or custom rule set. <br>
Mitigation: Review desensitized output before sharing and add custom rules for formats that are not covered by the built-in rule list. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bianchengyy/mitools-desensitize) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, configuration] <br>
**Output Format:** [Plain text and JSON; file mode can write a desensitized file and a mapping JSON file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit reversible mapping data that should be handled as sensitive.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
