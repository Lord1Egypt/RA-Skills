## Description: <br>
MT-Paotui-For-Client helps an agent collect details, preview fees, and submit Meituan errand orders for pickup and delivery, purchasing, queueing, moving, disposal, and other local help tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meituan-tech](https://clawhub.ai/user/meituan-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to manage Meituan errand-ordering workflows: authorization, address lookup, POI search, fee preview, explicit confirmation, order submission, and order-status checks. <br>

### Deployment Geography for Use: <br>
China mainland <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate real Meituan errand orders that may lead to payment obligations. <br>
Mitigation: Use the documented two-step flow: show a fee preview first, require explicit user confirmation before submitting, and require an extra confirmation for fees above 100 yuan. <br>
Risk: The workflow handles Meituan authorization, saved addresses, phone information, and order details. <br>
Mitigation: Install only from a trusted publisher, use the user's own authorized account, and review address, phone, fee, and service details before confirmation. <br>
Risk: Server security evidence reports heavily obfuscated local code and an under-disclosed CLIGuard updater or daemon. <br>
Mitigation: Review the packaged local code and updater behavior before deployment, and deploy only in an environment where this background behavior is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/meituan-tech/mt-paotui-for-client) <br>
- [README.md](README.md) <br>
- [Command reference](references/commands.md) <br>
- [Parameter reference](references/params.md) <br>
- [Error handling reference](references/errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with user-facing status messages and inline shell commands for local execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+ and uses Meituan account authorization before accessing addresses, previewing fees, or submitting orders.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
