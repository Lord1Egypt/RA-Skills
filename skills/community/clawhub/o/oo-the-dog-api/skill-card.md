## Description: <br>
The Dog API skill guides agents to use OOMOL's oo CLI connector for reading and managing The Dog API breeds, images, favourites, and votes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to operate a connected The Dog API account through the OOMOL connector, including read-only breed and image queries plus confirmed favourites and votes changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates a connected The Dog API account through OOMOL and requires sensitive account credentials to be available server-side. <br>
Mitigation: Install and use it only when the user trusts OOMOL and intentionally wants the agent to operate that connected account. <br>
Risk: Write and destructive actions can create or delete favourites and votes. <br>
Mitigation: Confirm the exact payload, target, and expected effect with the user before running write or destructive actions. <br>
Risk: Setup commands can install the oo CLI or initiate account login and connector setup. <br>
Mitigation: Run install, login, or connection steps only after an action fails for the matching setup reason or the user explicitly requests setup. <br>


## Reference(s): <br>
- [The Dog API homepage](https://thedogapi.com/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-the-dog-api) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the OOMOL oo CLI; connector responses are returned as JSON when the --json flag is used.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
