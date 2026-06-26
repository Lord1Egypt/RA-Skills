## Description: <br>
Priority-based message delivery with urgency levels over the Pilot Protocol network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send, triage, and process Pilot Protocol messages by priority prefix for urgent communications and SLA-oriented workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clearing the Pilot Protocol inbox can remove messages before they are reviewed or archived. <br>
Mitigation: Review, process, or archive inbox contents before running pilotctl --json inbox --clear, and avoid unattended use unless message loss is acceptable. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with bash command and script examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the pilot-protocol skill, the pilotctl binary on PATH, and a running Pilot Protocol daemon.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
