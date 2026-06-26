## Description: <br>
Geokeo lets an agent run forward and reverse geocoding through the OOMOL oo CLI using a connected Geokeo account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to geocode addresses or places and reverse-geocode coordinates from a connected Geokeo account without handling raw API tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates through an OOMOL-connected Geokeo account and may use sensitive credentials for live service actions. <br>
Mitigation: Use it only in the intended ClawHub/OOMOL connected-account context, inspect the live action schema before building payloads, and avoid exposing raw credentials. <br>
Risk: Actions marked as write can affect the connected Geokeo service account. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running write or destructive actions. <br>


## Reference(s): <br>
- [Geokeo homepage](https://geokeo.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs actions with JSON payloads and returns connector responses containing data and meta.executionId.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
