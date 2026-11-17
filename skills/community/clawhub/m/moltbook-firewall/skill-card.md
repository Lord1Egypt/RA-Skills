## Description:

Moltbook Firewall helps agents scan Moltbook and similar social content for prompt injection, social engineering, malicious code requests, and data exfiltration attempts before processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[machinesbefree](https://clawhub.ai/user/machinesbefree)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill as a defensive pre-processing check for social platform content. It flags known patterns for prompt injection, social engineering, malicious code execution requests, suspicious URLs, and data exfiltration attempts before an agent acts on external content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanned content previews are written to a local audit log, which can retain confidential prompts, credentials, customer data, or secrets if such content is scanned.

Mitigation: Do not scan confidential data unless logging is removed or made opt-in with redaction and restrictive file permissions.

Risk: The documented pattern customization and trusted-source controls are not fully enforced according to the security evidence.

Mitigation: Review and test the scanner before relying on custom rules, trusted-source lists, or the documented add-pattern workflow.

Risk: Pattern matching can miss novel or obfuscated attacks and can flag benign content that matches broad expressions.

Mitigation: Use scan results as a review gate, keep human review for SUSPICIOUS results, and update enforced patterns after validated incidents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/machinesbefree/skills/moltbook-firewall)
- [README](artifact/README.md)
- [Threat patterns](artifact/patterns/threats.json)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Terminal text with SAFE, SUSPICIOUS, or BLOCKED status and local JSONL audit log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scanner exits 0 for SAFE, 1 for SUSPICIOUS, and 2 for BLOCKED; scan logs include a local preview of the scanned content.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
