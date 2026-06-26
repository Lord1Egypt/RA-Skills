## Description: <br>
Create and share rendered markdown web pages through the Peekmd API with optional TTLs, rich formatting, auto-expiring links, and burn-after-read deletion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[notacryptodad](https://clawhub.ai/user/notacryptodad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, agents, bots, and developers use this skill to publish formatted markdown such as reports, docs, code snippets, tables, and diagrams as temporary shareable web pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Markdown uploaded to peekmd.dev could expose secrets, credentials, private customer data, regulated data, or internal-only reports. <br>
Mitigation: Do not send sensitive content and use short TTLs for temporary sharing. <br>
Risk: Paid tiers and x402 payment flows could trigger unintended commercial or crypto actions. <br>
Mitigation: Confirm any paid or crypto action before proceeding. <br>
Risk: Burn-after-read deletion could remove the wrong page if the slug is incorrect. <br>
Mitigation: Verify the slug before burning a page. <br>


## Reference(s): <br>
- [ClawHub Peekmd package page](https://clawhub.ai/notacryptodad/peekmd) <br>
- [Peekmd homepage](https://peekmd.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API endpoint choices, TTL recommendations, generated share URLs, and burn-after-read deletion guidance.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
