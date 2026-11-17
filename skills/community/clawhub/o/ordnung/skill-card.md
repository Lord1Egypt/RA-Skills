## Description:

Ordnung helps agents join and check a workspace-organization movement centered on structured files, persistent local notes, and optional service registration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[denis-sav](https://clawhub.ai/user/denis-sav)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to register with the ORDNUNG service, record local initiation notes, and check movement status. It is intended for users who explicitly want persistent workspace organization rituals and local agent memory updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The join flow can write persistent agent identity and memory files that may influence later sessions.

Mitigation: Review the exact SOUL.md and memory/ changes before running scripts/join.sh and approve each persistent change explicitly.

Risk: The skill encourages broad home-directory review, cleanup, commit, and delete rituals.

Mitigation: Restrict any cleanup or commit operation to clearly approved paths and avoid blanket commands over the home directory.

Risk: The join script contacts the ORDNUNG service and stores credentials locally.

Mitigation: Run only when service registration is intended, use ORDNUNG_API_BASE for local testing when needed, and treat ~/.config/ordnung/credentials.json as a secret.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/denis-sav/skills/ordnung)
- [ORDNUNG homepage](https://ordnung.church)
- [Join API endpoint](https://ordnung.church/api/join)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and local file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses curl, sha256sum, grep, and sed; optional environment variables configure manifesto text, agent name, referral code, and API base URL.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
