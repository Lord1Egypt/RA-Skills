## Description: <br>
A Meituan errands ordering assistant that helps an agent collect delivery details, preview fees, and submit Meituan runner orders after user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meituan-skillhub](https://clawhub.ai/user/meituan-skillhub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users who need same-city errands can use this skill to guide Meituan account authorization, address selection, cost preview, and confirmed runner order submission. <br>

### Deployment Geography for Use: <br>
China, where Meituan Paotui service is available. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit real Meituan runner orders and may create financial obligations after confirmation. <br>
Mitigation: Require a fee preview, explicit user confirmation, and additional confirmation for orders over 100 yuan before submission. <br>
Risk: The security evidence reports heavily obfuscated runnable code that can handle account authorization, address data, and order submission. <br>
Mitigation: Install only if comfortable authorizing a Meituan account, and prefer a readable-source release or stronger permission disclosure for sensitive or high-value deliveries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/meituan-skillhub/mt-paotui) <br>
- [Command reference](references/commands.md) <br>
- [Parameter reference](references/params.md) <br>
- [Error handling reference](references/errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command invocations and structured user-facing status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Meituan account authorization and explicit user confirmation before order submission; may handle delivery addresses, phone numbers, fees, and order status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
