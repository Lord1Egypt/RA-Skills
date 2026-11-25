## Description:

Read MyAtriumHealth test results, medications, allergies, immunizations, health issues, visits, goals, and messages through the signed-in patient portal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and developers use the skill to retrieve information from the active patient's Atrium Health MyChart account, including results, medications, visits, and messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review rates the release suspicious and flags health-portal cookie capture, persistent trust, and handling of an exported authentication token; the analysis is partial because two local references were unresolved.

Mitigation: Review the suspicious verdict before installation; approve access only when the bridge and requested cookie scope are trusted, revoke persistent trust when no longer needed, and avoid exposing MAH_TOKEN to untrusted child processes.

## Reference(s):

- [ClawHub release](https://clawhub.ai/chrischall/skills/myatriumhealth-mcp)
- [Endpoint recipes](artifact/references/endpoints.md)
- [Browser helper commands](artifact/references/mah.sh)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)
- [MyAtriumHealth portal](https://my.atriumhealth.org/)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, JSON data, Configuration instructions]

**Output Format:** [Markdown guidance, shell commands, and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses can contain personal health information and may need jq projection.]

## Skill Version(s):

1.6.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
