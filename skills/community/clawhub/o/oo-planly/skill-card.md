## Description:

Connect to Planly to list teams, channels, media, and schedules, import or delete media, and create scheduled social posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to inspect Planly teams, channels, media, and schedules, and to manage media and scheduled social posts through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup can add or synchronize additional agent skills, while remote installers and downloaded runtime are unverified.

Mitigation: Review the CLI installer before use, decide whether bundled skills are wanted, and use OO_SKILLS_SYNC_DISABLED to prevent startup skill synchronization when appropriate.

Risk: Using Planly entrusts the connected account credentials and requested operations to OOMOL.

Mitigation: Connect only an account intended for this use, confirm the exact effect before writes, and explicitly approve the target before destructive actions.

## Reference(s):

- [Planly API documentation](https://docs.planly.com/)
- [Planly homepage](https://planly.com)
- [oo CLI documentation and source](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [Planly data in JSON with concise textual summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-specific results; writes and destructive actions require user confirmation.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
