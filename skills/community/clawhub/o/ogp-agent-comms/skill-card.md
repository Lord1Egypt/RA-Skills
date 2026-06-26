## Description: <br>
Interactive wizard to configure agent-to-agent communication policies for federated peers, including multi-framework workflows, peer identity, and multi-agent routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dp-pcs](https://clawhub.ai/user/dp-pcs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure OGP agent-to-agent communication policies. It helps them set peer-specific topics, response levels, human delivery behavior, and multi-agent routing for federated agent messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad global defaults can let federated peers receive more detail than intended. <br>
Mitigation: Prefer per-peer and per-topic policies, and use summary, escalate, deny, or approval-required modes for sensitive topics. <br>
Risk: Full or autonomous response modes can allow replies without human review. <br>
Mitigation: Use the delegated-authority interview and require escalation or approval for untrusted peers and sensitive message classes. <br>
Risk: Activity logs can contain message contents and peer details. <br>
Mitigation: Treat activity logs as sensitive and restrict access according to local policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dp-pcs/ogp-agent-comms) <br>
- [OGP documentation](https://github.com/dp-pcs/ogp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with bash command examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces policy configuration guidance for an agent; no binary artifacts.] <br>

## Skill Version(s): <br>
0.6.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
