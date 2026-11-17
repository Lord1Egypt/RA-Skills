## Description:

Poly-Mal-Scan is a multilingual PHP, JavaScript, and Bash malware and webshell scanning skill that helps agents use CLI or MCP scanning, update rule libraries, and troubleshoot false positives or false negatives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsherryyann](https://clawhub.ai/user/tsherryyann)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to scan PHP, JavaScript, and Bash source code for malware, webshells, reverse shells, command injection, file-writing backdoors, and obfuscated payloads. Agents can also use it to mount or test the MCP scanner, tune signature rules, and run scanner workflows across supported languages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP scanner can read any file path available to its service account if exposed without a workspace boundary.

Mitigation: Run the MCP server under a low-privilege account, expose it only to trusted clients, and restrict scans to the intended workspace.

Risk: Optional parser dependencies affect scan depth; missing tree-sitter support can reduce AST-based detection coverage.

Mitigation: Pin and verify tree_sitter and tree_sitter_language_pack versions before deployment when full AST normalization is required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tsherryyann/skills/poly-mal-scan)
- [MITRE ATT&CK Enterprise Techniques](https://attack.mitre.org/techniques/enterprise/)
- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)
- [tennc/webshell](https://github.com/tennc/webshell)
- [GTFOBins](https://gtfobins.github.io/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scanner workflows return structured JSON results when invoked through the documented CLI, Python, or MCP paths.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
