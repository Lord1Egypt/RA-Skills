## Description: <br>
Use the mycelium CLI to join coordination rooms, negotiate with other agents via CognitiveEngine, and share persistent memory across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juliarvalenti](https://clawhub.ai/user/juliarvalenti) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Mycelium to coordinate multiple agents in shared rooms, run structured negotiations, and maintain persistent room memory across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores room memory as plaintext markdown files under ~/.mycelium/rooms and may sync those files to a configured backend. <br>
Mitigation: Do not store credentials, secrets, sensitive personal data, or private business data in room memory; use only trusted, access-controlled backends. <br>
Risk: The skill depends on a third-party CLI, Homebrew tap, and backend URL configured in ~/.mycelium/config.toml. <br>
Mitigation: Review and trust the mycelium CLI, the mycelium-io Homebrew tap, release artifacts, and configured backend before installation or use. <br>
Risk: Negotiation and coordination commands can influence shared plans used by multiple agents. <br>
Mitigation: Review proposed commands, consensus results, and generated task plans before acting on them in production workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/juliarvalenti/skills/mycelium-io) <br>
- [Mycelium project homepage](https://github.com/mycelium-io/mycelium) <br>
- [Homebrew tap](https://github.com/mycelium-io/homebrew-tap) <br>
- [Release v1.1.3](https://github.com/mycelium-io/mycelium/releases/tag/v1.1.3) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands assume the mycelium CLI is installed and configured with ~/.mycelium/config.toml.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
