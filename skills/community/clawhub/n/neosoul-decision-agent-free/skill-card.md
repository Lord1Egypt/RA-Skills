## Description: <br>
自主决策代理 is a local decision-support skill that helps users structure tradeoff analysis, maintain local decision memory, and review past decisions without making the final decision for them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and teams can use this skill to analyze product, technical architecture, business strategy, or personal decisions with structured options, confidence labels, and local decision-review records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create a ./decision-making/ folder and store persistent decision history locally. <br>
Mitigation: Use it only in workspaces where local decision records are acceptable, and review or remove stored records before sharing the workspace. <br>
Risk: Decision records could include secrets, customer data, or sensitive third-party information if users provide that content. <br>
Mitigation: Do not include secrets, customer data, or sensitive third-party information in prompts or saved decision records. <br>
Risk: The release contains inconsistent callback_url and API_KEY documentation. <br>
Mitigation: Treat callback and credential setup as unresolved until the publisher clarifies whether any network callback or credential is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/neosoul-decision-agent-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown decision analysis with optional shell commands and local file records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and update local files under ./decision-making/ for memory and decision review records.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
