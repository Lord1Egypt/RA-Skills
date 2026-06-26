## Description: <br>
Guides agents to use OOMOL's oo CLI for Finage connector actions, including live schema inspection and U.S. stock market data retrieval through a connected Finage account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to route Finage requests through an OOMOL-connected account, inspect action schemas, and retrieve U.S. stock aggregates, quotes, trades, previous close data, snapshots, and symbol listings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a connected Finage account and may operate on sensitive credentials through OOMOL. <br>
Mitigation: Install it only when the agent should use the connected Finage account, and keep raw credentials outside the agent workflow. <br>
Risk: Broad Finage requests or actions tagged as write could lead to unintended state-changing operations. <br>
Mitigation: Inspect the live action schema and confirm the exact payload and effect before allowing updates or other state-changing actions. <br>


## Reference(s): <br>
- [Finage homepage](https://finage.co.uk) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-finage) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
