## Description: <br>
Picoclaw-only local posture-review skill focused on read-only findings and safe operator remediation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davida-ps](https://clawhub.ai/user/davida-ps) <br>

### License/Terms of Use: <br>
AGPL-3.0-or-later <br>


## Use Case: <br>
Picoclaw operators and security reviewers use this skill to run local, read-only posture checks against an existing Picoclaw profile and review severity-ranked findings with remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The profile file may contain sensitive local security configuration details. <br>
Mitigation: Handle the profile as sensitive input and avoid sharing generated findings or profile excerpts without review. <br>
Risk: Optional release-verification commands download artifacts from GitHub before checksum and signature validation. <br>
Mitigation: Review the commands before running them and only install or extract the archive after verification succeeds. <br>
Risk: The skill reports security findings but does not perform remediation. <br>
Mitigation: Treat recommendations as operator review guidance and require explicit approval before making configuration changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davida-ps/picoclaw-self-pen-testing) <br>
- [ClawSec homepage](https://clawsec.prompt.security) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, json, guidance, shell commands] <br>
**Output Format:** [JSON findings with severity counts and per-finding recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally on a user-specified Picoclaw profile; no hidden persistence or network activity is described by the security evidence.] <br>

## Skill Version(s): <br>
0.0.2 (source: frontmatter, skill.json, changelog, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
