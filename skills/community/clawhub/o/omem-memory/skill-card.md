## Description:

OMEM memory gives an agent self-hosted belief-revision memory for remembering durable facts with provenance, checking belief state, preserving contradictions, and producing evidence-chain explanations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[troybrandonc-bit](https://clawhub.ai/user/troybrandonc-bit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when an agent needs persistent, auditable memory for facts about people, entities, preferences, and claims across sessions. It is suited to workflows that need contradiction detection before acting on remembered information and evidence-chain explanations for why a belief is held.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent agent memory can retain sensitive, outdated, or disputed information if users store credentials, one-off data, or unresolved facts.

Mitigation: Store only durable facts, avoid credentials and sensitive one-off data, check belief state before acting, and surface contradicted states to the user.

Risk: The skill depends on a user-controlled OMEM server and an external server package, so endpoint exposure or an unreviewed package could affect confidentiality and reliability.

Mitigation: Prefer a local loopback server or HTTPS for remote use, pin and review the omem-infrastructure package before installation, and protect OMEM_API_KEY and OMEM_PROJECT.

## Reference(s):

- [OMEM memory ClawHub release](https://clawhub.ai/troybrandonc-bit/skills/omem-memory)
- [Third-party publisher profile](https://clawhub.ai/user/troybrandonc-bit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples; OMEM commands return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OMEM_API_KEY and OMEM_PROJECT, with OMEM_BASE_URL defaulting to a local self-hosted server.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
