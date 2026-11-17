## Description:

Unsafe deserialization vulnerability scanner (OWASP A08:2021). Detects Python pickle/yaml/eval, Java ObjectInputStream/XStream/XMLDecoder, PHP unserialize, Ruby Marshal.load, Node.js eval/new Function/vm, Go gob with interface{}. Traces HTTP input sources to dangerous sinks, classifies CRITICAL/HIGH/MEDIUM, outputs CWE/CVE mappings and per-language fix snippets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to scan source repositories for unsafe deserialization patterns, nearby HTTP input sources, severity classifications, CWE/CVE mappings, and remediation snippets across Python, Java, PHP, Ruby, Node.js/TypeScript, and Go.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented Python snippet may need correction before operational use.

Mitigation: Review and fix the snippet in a controlled repository before relying on scan results.

Risk: The scanner reads source files in the target repository to produce findings.

Mitigation: Run it only on repositories the user intends to scan and is authorized to inspect.

Risk: Static findings can misclassify data flow or miss context around trusted inputs.

Mitigation: Review reported taint context and remediation guidance before making security decisions.

## Reference(s):

- [OWASP A08:2021 - Software and Data Integrity Failures](https://owasp.org/A08_2021-Software_and_Data_Integrity_Failures/)
- [Canlah AI](https://canlah.ai)
- [ClawHub publisher profile](https://clawhub.ai/user/phy041)
- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-deserialization-audit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Python, shell, JSON, and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include severity, CWE/CVE mappings, taint context, and per-language fix guidance.]

## Skill Version(s):

1.0.3 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
