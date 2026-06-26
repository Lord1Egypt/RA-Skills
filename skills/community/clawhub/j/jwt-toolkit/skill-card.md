## Description: <br>
Decodes and inspects JWT tokens from the command line, showing headers, payload claims, algorithm details, expiry status, and known claim labels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to decode raw or Bearer JWTs during authentication debugging, inspect claims and algorithm metadata, and check expiration status without external dependencies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real JWTs can contain sensitive authentication data and may be exposed through shared terminals, logs, shell history, or support chats. <br>
Mitigation: Use disposable or redacted token examples when possible, and avoid pasting live tokens into shared or logged environments. <br>
Risk: The tool decodes tokens and checks expiry, but it does not prove that a token is trustworthy. <br>
Mitigation: Verify signatures, issuer, audience, keys, and authorization decisions with the relevant authentication system before relying on a token. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Johnnywang2001/jwt-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the helper script emits text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports direct token input, files, stdin, Bearer prefixes, and text or JSON output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
