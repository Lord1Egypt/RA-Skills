## Description:

Interact with Radarr via its REST API for searching movies, checking missing or wanted titles, triggering downloads, and monitoring queue status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minerva-care](https://clawhub.ai/user/minerva-care)

### License/Terms of Use:

MIT-0

## Use Case:

External users and media automation operators use this skill to have an agent inspect and operate a Radarr movie manager through documented REST API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated Radarr operations can add movies, trigger bulk missing-movie searches, delete items, blacklist queue entries, rename files, or rescan libraries.

Mitigation: Require explicit user confirmation before mutating or bulk actions, especially POST command calls and DELETE endpoints.

Risk: A leaked Radarr API key could allow unintended access to the configured Radarr instance.

Mitigation: Keep the API key secret, load it from a local credentials file, and restrict agent use to the intended local Radarr server.

## Reference(s):

- [Radarr API Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/minerva-care/skills/minerva-radarr)
- [Publisher Profile](https://clawhub.ai/user/minerva-care)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include authenticated Radarr API calls and credential handling guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
