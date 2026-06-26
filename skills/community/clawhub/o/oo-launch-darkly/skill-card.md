## Description: <br>
Operates LaunchDarkly through OOMOL's launch_darkly connector to read, create, update, and delete LaunchDarkly resources instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, release managers, and operations teams use this skill to manage LaunchDarkly projects, environments, feature flags, segments, teams, members, access tokens, tags, contexts, and caller identity through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write actions can change LaunchDarkly projects, environments, feature flags, segments, teams, and access tokens. <br>
Mitigation: Review the exact payload and expected effect with the user before approving write actions. <br>
Risk: Destructive actions can delete LaunchDarkly resources or reset access token values, affecting production feature flags, access, or account configuration. <br>
Mitigation: Require explicit confirmation of the target resource before deletes, token resets, and token creation. <br>
Risk: The skill requires OAuth-connected LaunchDarkly access and sensitive credentials are handled through the OOMOL connector. <br>
Mitigation: Install only when the agent should manage LaunchDarkly through the user's OOMOL connection, and keep authority scoped to that connection. <br>


## Reference(s): <br>
- [ClawHub LaunchDarkly skill page](https://clawhub.ai/oomol/oo-launch-darkly) <br>
- [LaunchDarkly homepage](https://launchdarkly.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke LaunchDarkly connector actions through the oo CLI after inspecting live action schemas.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
