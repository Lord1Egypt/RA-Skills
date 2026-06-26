## Description: <br>
Updates Mihomo site routing rules from natural-language requests, rebuilds the published subscription, and verifies the live output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[grey0758](https://clawhub.ai/user/grey0758) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to turn requested domain or site routing changes into Mihomo rule edits, worker redeployments, subscription syncs, and live verification for rules.xiannai.me. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live routing changes can affect client-visible subscription behavior. <br>
Mitigation: Require the agent to show exact file changes and get explicit approval before deploy, sync, restart, commit, or push actions. <br>
Risk: Deployment and repository steps may involve Cloudflare or GitHub credentials. <br>
Mitigation: Install and run the skill only in an environment where the operator controls the referenced Mihomo repository, rules.xiannai.me deployment, and related credentials; never reveal token values. <br>
Risk: Repository state and live subscription output can diverge if publishing or sync fails. <br>
Mitigation: Verify the live subscription endpoint with cache busting and report any pending action instead of declaring success. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/grey0758/mihomo-subscription-route-publisher) <br>
- [Mihomo subscription distribution layer](https://rules.xiannai.me) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown status response with the normalized routing request, changed files, publish status, live verification result, and any pending next action.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Mihomo configuration edits, shell commands, deployment steps, sync commands, and validation results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
