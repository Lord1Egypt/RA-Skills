## Description: <br>
Operates Honeybadger through an OOMOL-connected account to report check-ins, deployments, Insights events, and exception notices using the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to submit Honeybadger check-ins, deployment reports, Insights events, and exception notices through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit Honeybadger check-ins, deployments, events, and exception notices. <br>
Mitigation: Treat every report_* action as a write, inspect the live connector schema, and require explicit user confirmation of the exact payload before execution. <br>
Risk: The skill relies on connected Honeybadger credentials through OOMOL. <br>
Mitigation: Install only for users who intend to use OOMOL with Honeybadger, and retry setup only after authentication, connection, scope, app readiness, or billing failures. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-honeybadger) <br>
- [Honeybadger Homepage](https://www.honeybadger.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the oo CLI, an OOMOL account, and a connected Honeybadger credential; report actions can submit data to Honeybadger.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
