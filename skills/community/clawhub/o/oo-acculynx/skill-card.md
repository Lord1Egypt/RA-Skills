## Description: <br>
AccuLynx helps an agent operate AccuLynx through an OOMOL-connected account to read business data and create or update contacts, Lead-milestone jobs, and initial appointments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or teams with an OOMOL-connected AccuLynx account use this skill to inspect live AccuLynx schemas, read company configuration and calendar data, and perform guarded write actions such as creating contacts, creating Lead-milestone jobs, or upserting initial appointments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or update records in AccuLynx, including contacts, Lead-milestone jobs, and initial appointments. <br>
Mitigation: Confirm every write action, target, payload, and expected effect with the user before running the connector command. <br>
Risk: The release requires sensitive AccuLynx and OOMOL credentials and was flagged for review because it combines broad invocation language with write-capable business-system access. <br>
Mitigation: Use a least-privileged AccuLynx/OOMOL account and install only when the agent is intended to operate AccuLynx through OOMOL. <br>
Risk: The first-time setup guidance includes a pipe-to-shell installer fallback for the oo CLI. <br>
Mitigation: Prefer installing the CLI through a trusted, verified path and avoid letting the agent run the remote installer automatically. <br>


## Reference(s): <br>
- [ClawHub AccuLynx Skill Page](https://clawhub.ai/oomol/oo-acculynx) <br>
- [AccuLynx Homepage](https://acculynx.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL AccuLynx Connections](https://console.oomol.com/app-connections?provider=acculynx) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads; write actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
