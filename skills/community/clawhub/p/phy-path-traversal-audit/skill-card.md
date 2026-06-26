## Description: <br>
Path traversal and Local File Inclusion (LFI) vulnerability scanner for detecting user-controlled paths passed to filesystem sinks in Python, Java, PHP, Node.js, Go, and Ruby without containment checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to audit codebases for path traversal, local file inclusion, and zip-slip patterns and to get language-specific remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the embedded script appears broken as written, so scan results may be unreliable. <br>
Mitigation: Verify or fix the embedded Python before relying on its findings or using it in CI. <br>
Risk: The skill scans local repositories and needs filesystem access to the target source tree. <br>
Mitigation: Run it only against repositories you intend to audit and avoid granting credentials, network access, background service privileges, or broader system access. <br>


## Reference(s): <br>
- [Canlah AI homepage](https://canlah.ai) <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-path-traversal-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with findings, CLI examples, JSON-output option, and remediation snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings may include severity, CWE, file path, line number, matched pattern, HTTP taint signal, risk description, and fix guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
