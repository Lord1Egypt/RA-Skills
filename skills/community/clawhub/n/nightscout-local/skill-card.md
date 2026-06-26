## Description: <br>
Read glucose data from a Nightscout site for current CGM readings, trends, recent readings, or basic Nightscout status while staying read-only. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xeusoc](https://clawhub.ai/user/xeusoc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve read-only glucose readings and Nightscout site status from a user-configured Nightscout base URL. It is intended for reporting readings clearly, not for modifying Nightscout settings or providing medical advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Glucose readings are sensitive health data and may appear in the agent conversation. <br>
Mitigation: Treat readings as private health information and avoid sharing conversation output beyond the intended user and authorized systems. <br>
Risk: The skill depends on the user-configured Nightscout site and may return stale, unavailable, or incomplete data if the endpoint is misconfigured or down. <br>
Mitigation: Configure NIGHTSCOUT_BASE_URL or pass --url for the intended Nightscout site, and report endpoint failures plainly. <br>
Risk: A separate current_bg.py helper is referenced but was not part of the inspected release evidence. <br>
Mitigation: Inspect that local helper before use or prefer the bundled scripts/nightscout_read.py command. <br>


## Reference(s): <br>
- [ClawHub Nightscout-Local release page](https://clawhub.ai/xeusoc/nightscout-local) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown or plain text response summarizing JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports glucose in mg/dL with trend and timestamp when available; requires a configured Nightscout base URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
