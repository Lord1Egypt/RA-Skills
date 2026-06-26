## Description: <br>
Healthchecks.io lets agents operate Healthchecks.io checks through OOMOL's oo CLI, including reading, creating, updating, pausing, resuming, and deleting checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Healthchecks.io monitoring checks from an OOMOL-connected account. It supports project visibility, check lifecycle operations, notification channel review, status flips, and recent ping inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a connected Healthchecks.io API key through OOMOL. <br>
Mitigation: Install only after confirming trust in OOMOL and comfort with the Healthchecks.io account connection. <br>
Risk: Create, update, pause, resume, and delete actions can affect monitoring state or remove checks. <br>
Mitigation: Confirm the exact target and payload with the user before approving write or destructive actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-healthchecks-io) <br>
- [Healthchecks.io Homepage](https://healthchecks.io) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON connector payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are returned as JSON with data and meta.executionId fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
