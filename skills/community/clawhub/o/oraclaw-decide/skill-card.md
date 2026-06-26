## Description: <br>
Decision intelligence for AI agents. Analyze options, map decision dependencies with PageRank, detect when information sources conflict, and find the choices that matter most. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whatsonyourmind](https://clawhub.ai/user/whatsonyourmind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use Oraclaw Decide to choose among competing options, analyze decision dependencies, identify bottlenecks or critical paths, and compare source agreement before making strategic decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an external decision-analysis service with an API key and paid per-call usage. <br>
Mitigation: Use a revocable ORACLAW_API_KEY, monitor billing, and rotate or revoke the key when it is no longer needed. <br>
Risk: Decision inputs may contain confidential or regulated information sent to the external provider. <br>
Mitigation: Review the provider's privacy and retention terms before use and avoid sending sensitive decision data unless approved. <br>
Risk: Decision recommendations can be affected by incomplete inputs or conflicting sources. <br>
Mitigation: Review outliers and source disagreement before acting, especially when convergence scoring reports a large spread. <br>


## Reference(s): <br>
- [OraClaw Decide homepage](https://oraclaw.dev/decide) <br>
- [ClawHub skill page](https://clawhub.ai/whatsonyourmind/oraclaw-decide) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ORACLAW_API_KEY for external service calls; pricing evidence states $0.05 USDC per analysis call with a 100 decisions/month free tier.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
