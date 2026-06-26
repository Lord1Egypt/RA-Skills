## Description: <br>
Max Banking helps OpenClaw users connect a Max Bank account, check balance, create PIX payment requests, and create boleto payment requests from text or decoded QR/barcode inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jonatancosta](https://clawhub.ai/user/jonatancosta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Max Bank/OpenClaw users use this skill to perform banking workflows through an agent: account pairing, balance lookup, PIX payment request creation, and boleto payment request creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PIX and boleto requests can be created from broad or ambiguous text, uploaded images, QR codes, or numeric inputs. <br>
Mitigation: Require explicit user confirmation before every PIX or boleto execution, narrow automatic triggers, and disable automatic handling of uploaded images and raw numbers in sensitive deployments. <br>
Risk: The skill stores a long-lived MaxBank agent_key locally and uses it to call the banking MCP endpoint. <br>
Mitigation: Protect the credential as a banking secret, keep restrictive filesystem permissions, rotate or revoke it if exposed, and install only when the publisher and MCP endpoint are trusted. <br>
Risk: Status or debug output may expose internal configuration, account, endpoint, or credential-adjacent details. <br>
Mitigation: Do not show script commands, raw status output, paths, secrets, ports, or identifiers to end users. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jonatancosta/max-banking) <br>
- [Publisher profile](https://clawhub.ai/user/jonatancosta) <br>
- [Manifest homepage](https://github.com/maxter/mcp-payment-skill) <br>
- [Manifest support URL](https://github.com/maxter/mcp-payment-skill/issues) <br>
- [MaxBank production MCP health check](https://maxbank-mcp.max.com.br/health) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational text with internal shell commands and JSON responses from scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates real PIX and boleto payment requests through the MaxBank MCP endpoint; final approval is expected in WhatsApp or the Max app.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, artifact manifest, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
