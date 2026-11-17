## Description:

Data desensitization tool for masking phone numbers, ID cards, bank cards, email addresses, IP addresses, Chinese names, path usernames, long digit sequences, field names, and custom wildcard matches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bianchengyy](https://clawhub.ai/user/bianchengyy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to mask sensitive content in text, files, logs, shared data, test data, and documents, and to restore masked values when a mapping table is intentionally retained.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reversible plaintext mapping files can expose original sensitive data.

Mitigation: Run the skill in a private directory, treat .mapping.json files as sensitive secrets, and protect or delete mapping files immediately after use.

Risk: Restoration requires sharing a mapping JSON that contains original-to-masked value relationships.

Mitigation: Share mapping data only with trusted operators and avoid passing mappings to agents or third parties unless restoration is required and approved.

Risk: File mode may write desensitized output and a related mapping file beside the source or output path.

Mitigation: Choose explicit output locations and avoid running file mode on highly sensitive data unless the residual restoration risk is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bianchengyy/skills/mitools-desensitize)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Plain text or file output with JSON mapping data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [File mode may create a .mapping.json file that enables restoration of masked values.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
