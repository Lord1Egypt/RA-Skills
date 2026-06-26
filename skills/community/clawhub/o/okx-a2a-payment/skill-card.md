## Description: <br>
Use this skill when the user mentions creating a payment link, paying a paymentId / a2a_... link, or checking a2a payment status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ok-james-01](https://clawhub.ai/user/ok-james-01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create, pay, and check internal Onchain OS agent-to-agent payment links with the `onchainos payment a2a-pay` CLI. Buyer-side payment authorization depends on an upstream check that the paymentId matches the expected amount, token, recipient, and seller. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can authorize wallet payments from a paymentId without its own payment-detail preview or final confirmation step. <br>
Mitigation: Before invoking payment, independently verify the paymentId against the expected amount, token, recipient, and seller, and use only a wallet intended for agent payments. <br>
Risk: The skill shells out to `onchainos payment a2a-pay` for payment creation, signing, and status checks. <br>
Mitigation: Use the skill only with a trusted `onchainos` CLI installation and confirm the wallet session with `onchainos wallet status` before create or pay operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ok-james-01/okx-a2a-payment) <br>
- [Publisher profile](https://clawhub.ai/user/ok-james-01) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include payment IDs, delivery URLs, transaction hashes, block numbers, payment status, and fee displays.] <br>

## Skill Version(s): <br>
3.1.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
