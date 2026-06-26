## Description: <br>
Doppler (doppler.com). Use this skill for ANY Doppler request - reading, creating, updating, and deleting data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect Doppler connector schemas and run Doppler project, environment, config, secret, service token, sync, and change request actions through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose Doppler secret values and perform major account changes when requested. <br>
Mitigation: Use a least-privilege Doppler connection and review exact targets before approving write, token, sync, or delete operations. <br>
Risk: Write and destructive actions can change or remove Doppler projects, configs, environments, secrets, service tokens, syncs, and dynamic secret leases. <br>
Mitigation: Confirm the exact payload and target before running write actions, and require explicit approval before destructive actions. <br>


## Reference(s): <br>
- [Doppler homepage](https://www.doppler.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Doppler connection settings](https://console.oomol.com/app-connections?provider=doppler) <br>
- [Doppler skill on ClawHub](https://clawhub.ai/oomol/oo-doppler) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return Doppler connector JSON responses when actions are executed.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
