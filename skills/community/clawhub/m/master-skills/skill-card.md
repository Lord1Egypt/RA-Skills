## Description: <br>
Secure key management for AI agents that handle private keys, API secrets, wallet credentials, or agent-controlled funds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allprogramming9999](https://clawhub.ai/user/allprogramming9999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to guide agents that need safer handling of secrets, wallet credentials, and bounded session-key access. It focuses on secret storage, leak prevention, output sanitization, and prompt-injection defenses around credential-sensitive workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may be given access to high-impact secrets or wallet credentials. <br>
Mitigation: Use a dedicated 1Password vault, short-lived session keys with spending limits, and human review for high-impact credential or transaction use. <br>
Risk: Credential material could be exposed through logs, files, or agent outputs. <br>
Mitigation: Retrieve secrets at runtime through `op`, avoid storing raw keys in workspace files, and apply output sanitization before messages, logs, or file writes. <br>
Risk: Prompt injection could try to extract keys or trigger unauthorized wallet operations. <br>
Mitigation: Validate inputs, keep wallet-sensitive operations isolated from conversation context, and use allowlisted bounded operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/allprogramming9999/master-skills) <br>
- [Publisher profile](https://clawhub.ai/user/allprogramming9999) <br>
- [Project homepage](https://numbergroup.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the 1Password CLI (`op`) for workflows that retrieve secrets at runtime.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
