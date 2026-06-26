## Description: <br>
Space and astronomy data source skill for querying NASA Astronomy Picture of the Day and Open Notify astronauts through Pilot Protocol service agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
External users and developers use this skill to discover Pilot Protocol space-data agents, inspect their filter contracts, and run pilotctl queries for APOD metadata, media URLs, or the current list of astronauts in space. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow depends on a local pilotctl binary, a running Pilot Protocol daemon, and participation in the Pilot Protocol overlay network. <br>
Mitigation: Install and run the skill only when the Pilot Protocol tooling and network configuration are trusted for the target environment. <br>
Risk: Agent responses can include third-party media URLs or Gemini-generated summaries that may be incomplete, external, or unsuitable as authoritative results. <br>
Mitigation: Treat returned links and summaries as external content, and verify important results against the upstream data source before relying on them. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-service-agents-space) <br>
- [Pilot skills catalog](https://teoslayer.github.io/pilot-skills/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands use pilotctl and may require a follow-up inbox read to retrieve JSON envelopes, plain text help, or generated summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
