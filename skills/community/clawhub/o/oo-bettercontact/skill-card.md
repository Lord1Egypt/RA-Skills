## Description: <br>
BetterContact (bettercontact.rocks) lets an agent check account credit balance, submit leads for waterfall enrichment, and poll enrichment results through an OOMOL-connected BetterContact account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate BetterContact enrichment from an agent without handling raw API tokens. It is suited for checking BetterContact credits, submitting lead enrichment requests, and retrieving enrichment status or results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires use of an OOMOL-connected BetterContact account. <br>
Mitigation: Install only when the agent should be allowed to use that connected account. <br>
Risk: Submitting enrichment requests can spend BetterContact credits and send lead data to BetterContact. <br>
Mitigation: Review and approve the exact enrichment payload before write actions are run. <br>
Risk: Connector contracts can change over time. <br>
Mitigation: Inspect the live action schema before building each payload. <br>


## Reference(s): <br>
- [ClawHub BetterContact Skill Page](https://clawhub.ai/oomol/oo-bettercontact) <br>
- [BetterContact Homepage](https://bettercontact.rocks) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
