## Description: <br>
Razorpay helps agents operate Razorpay through an OOMOL-connected account for reading, creating, and updating payment, order, and refund data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect Razorpay schemas and run Razorpay connector actions through the oo CLI for orders, payments, and refunds. The skill is intended for accounts where Razorpay has already been connected through OOMOL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create Razorpay orders and refunds, which are real payment-related write operations. <br>
Mitigation: Review the exact payload and get explicit user approval before running write actions such as order or refund creation. <br>
Risk: The skill requires an OOMOL-connected Razorpay account and therefore depends on sensitive account credentials managed outside the skill. <br>
Mitigation: Install only when OOMOL's oo CLI should access the user's Razorpay account, and reconnect only when an auth or connection failure requires it. <br>
Risk: Incorrect action payloads can produce unintended financial or operational effects. <br>
Mitigation: Fetch the live connector schema before building payloads and compare the request with the user's intended order, payment, or refund operation. <br>


## Reference(s): <br>
- [ClawHub Razorpay skill](https://clawhub.ai/oomol/oo-razorpay) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Razorpay homepage](https://razorpay.com) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands run through the oo CLI and return JSON responses that include data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
