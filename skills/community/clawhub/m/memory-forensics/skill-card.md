## Description: <br>
Memory forensics with Volatility and related tools. Acquire RAM dumps, extract processes and DLLs, investigate rootkits and fileless malware, recover credentials from memory, and reconstruct timelines from memory images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomonneas](https://clawhub.ai/user/solomonneas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security engineers, incident responders, and forensic analysts use this skill for authorized memory acquisition and RAM-dump analysis, including process, network, DLL, injection, rootkit, credential, and timeline investigations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory images and command outputs may expose passwords, hashes, tokens, private user activity, and malware artifacts. <br>
Mitigation: Use the skill only for authorized incident response, forensic, or lab work; store outputs securely, restrict access, redact before sharing, and rotate any exposed credentials. <br>
Risk: Live memory acquisition and credential-recovery steps can require elevated privileges and may affect forensic handling if run without preparation. <br>
Mitigation: Confirm authorization and scope before acquisition, minimize acquisition footprint, document tool use and timestamps, hash memory dumps, and maintain chain-of-custody records. <br>


## Reference(s): <br>
- [Memory Forensics skill page](https://clawhub.ai/solomonneas/memory-forensics) <br>
- [Volatility 3 symbol downloads](https://downloads.volatilityfoundation.org/volatility3/symbols/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command and code examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance can lead to forensic artifacts and command outputs containing sensitive memory contents.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
