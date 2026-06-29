## Description: <br>
Shippo (goshippo.com). Use this skill for ANY Shippo request - reading, creating, and updating data. Whenever a task involves Shippo, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Shippo through an OOMOL-connected account for shipping workflows such as reading addresses and parcels, creating address or parcel objects, validating addresses, and checking tracking status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create Shippo addresses and parcels, which changes state in the connected Shippo account. <br>
Mitigation: Confirm write payloads and intended effects with the user before running actions tagged [write]. <br>
Risk: Shippo workflows can expose addresses, parcel details, tracking information, and account connection state. <br>
Mitigation: Treat shipping and account data as sensitive and share only what is needed for the user's request. <br>
Risk: First-time setup may require installing the oo CLI or connecting a Shippo account. <br>
Mitigation: Run setup or account connection steps only after an auth, connection, or missing-command failure and only from trusted sources. <br>


## Reference(s): <br>
- [Shippo homepage](https://goshippo.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands return JSON responses from the OOMOL Shippo connector when run with --json.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
