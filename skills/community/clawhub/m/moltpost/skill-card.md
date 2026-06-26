## Description: <br>
Send real physical postcards anywhere in the world. Pay with x402 (USDC on Base), Stripe, or manual USDC transfer. No signup, no API key -- just one API call. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cktc](https://clawhub.ai/user/cktc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use Moltpost to compose, pay for, and send physical postcards through Moltpost's API. The skill guides agents through recipient collection, postcard content creation, payment handling, status checks, and privacy-aware approval steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports paid, real-world postcard sending and handles recipient addresses and postcard content. <br>
Mitigation: Require explicit owner approval for each postcard, confirm recipient details, content, size, and cost before calling the API, and set postcards private when appropriate. <br>
Risk: Wallet signatures, onchain transfers, and payment links can spend funds or trigger fulfillment. <br>
Mitigation: Require explicit approval for each wallet signature or transfer, and present Stripe payment links to the human owner instead of completing payment on their behalf. <br>
Risk: The heartbeat routine fetches mutable remote instructions. <br>
Mitigation: Disable or tightly constrain heartbeat use unless the fetched instructions can be inspected and trusted. <br>
Risk: Postcards are physically unsealed and may be visible during handling and delivery. <br>
Mitigation: Avoid sensitive personal, financial, authentication, medical, legal, or children's information in postcard content. <br>


## Reference(s): <br>
- [Moltpost homepage](https://moltpost.io) <br>
- [Moltpost API base](https://api.moltpost.io/v1) <br>
- [Moltpost skill source](https://moltpost.io/skill.md) <br>
- [Moltpost heartbeat instructions](https://moltpost.io/heartbeat.md) <br>
- [Moltpost on ClawHub](https://clawhub.ai/cktc/moltpost) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, HTML, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown guidance with inline JSON, HTML, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions for paid postcard creation, payment workflows, status polling, and content safety checks.] <br>

## Skill Version(s): <br>
1.3.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
