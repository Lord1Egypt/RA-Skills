## Description:

Collects AI news, validates stage1 JSON, publishes KeplerJAI bulletins, and formats a final summary for an agent workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renjicode](https://clawhub.ai/user/renjicode)

### License/Terms of Use:

MIT-0

## Use Case:

External publishers and operators use this skill to gather AI news candidates, publish seven KeplerJAI bulletin entries through the KeplerJAI API, and produce a final text summary for review or sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make live authenticated KeplerJAI bulletin posts without confirmation.

Mitigation: Require explicit confirmation or dry-run review before production posting, especially for scheduled or automated runs.

Risk: Endpoint, header, and TLS override controls can weaken request boundaries.

Mitigation: Restrict execution to the real KeplerJAI HTTPS endpoint and remove or disable --insecure and arbitrary endpoint/header overrides before deployment.

Risk: The skill depends on bearer tokens or cookies for authenticated publishing.

Mitigation: Use narrowly scoped credentials from environment variables and avoid storing credentials in skill files or logs.

Risk: Implicit invocation and scheduled execution can publish content under the user's account at the wrong time or workspace.

Mitigation: Avoid implicit invocation for publish runs and bind scheduled tasks to the intended owner workspace with auditable pipeline logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/renjicode/skills/keplerjai-bulletin-publish)
- [NewsNow AI news source](https://www.newsnow.co.uk/h/Science/AI?type=ln)
- [KeplerJAI bulletin API](https://www.keplerjai.com/api/content/bulletin)
- [KeplerJAI bulletin frontend](https://www.keplerjai.com/bulletin?id=<bulletin_id>)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text final summary, JSON intermediate files, and shell-command/configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes stage artifacts such as stage1-output.txt, stage1-output.normalized.json, publish-result.json, final-message.txt, and pipeline.log in the agent workspace.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
