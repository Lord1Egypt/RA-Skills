## Description: <br>
Signalbase (trysignalbase.com) lets agents search and read Signalbase company, investor, acquisition, funding, hiring, and job-change data through the OOMOL-connected Signalbase connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query Signalbase through an OOMOL-connected account for company profiles, investor data, acquisition signals, funding signals, hiring signals, and job-change signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an OOMOL-connected Signalbase account and requires sensitive credential-backed access. <br>
Mitigation: Review requested permissions at install time, use the existing OOMOL connection, and avoid exposing raw tokens in prompts, logs, or command arguments. <br>
Risk: Connector payloads could be malformed or drift from the live Signalbase action contract. <br>
Mitigation: Inspect the live action schema before each connector run and build JSON payloads from that schema. <br>
Risk: Future connector actions may include write or destructive behavior even though the listed actions are read-oriented. <br>
Mitigation: Confirm the exact payload and effect with the user before any action tagged write, and require explicit approval before any destructive action. <br>


## Reference(s): <br>
- [Signalbase homepage](https://www.trysignalbase.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-signalbase) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and connector JSON response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill instructs the agent to inspect live connector schemas before sending JSON payloads and to return read-oriented Signalbase results from the connector response.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
