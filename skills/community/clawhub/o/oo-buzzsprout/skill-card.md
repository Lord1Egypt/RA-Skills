## Description:

Manage Buzzsprout podcasts and episodes by reading, creating, and updating data through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents managing a connected Buzzsprout account can inspect podcasts, episodes, and download statistics, and create or update episode and podcast data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path may make broader changes to the agent environment, and remote installer payloads are unverified.

Mitigation: Review and install the CLI separately, and consider disabling automatic skill synchronization with OO_SKILLS_SYNC_DISABLED=1.

Risk: Connecting Buzzsprout entrusts OOMOL with the integration's credentials and data.

Mitigation: Connect only an account whose credentials and data you are comfortable entrusting to OOMOL.

Risk: Creating or changing podcast and episode data can publish, schedule, or overwrite content.

Mitigation: Keep the skill's approval checks and confirm the exact target and changes before write or destructive actions.

## Reference(s):

- [Buzzsprout](https://www.buzzsprout.com)
- [Buzzsprout API documentation](https://github.com/buzzsprout/buzzsprout-api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [Buzzsprout ClawHub release](https://clawhub.ai/oomol/skills/oo-buzzsprout)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON action results and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by Buzzsprout action.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
