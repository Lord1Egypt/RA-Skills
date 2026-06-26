## Description: <br>
RAWG provides agent access to RAWG video game database search and lookup actions through OOMOL's oo CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to search RAWG and retrieve game, developer, platform, publisher, store, tag, media, and related-game data through an OOMOL-connected RAWG account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RAWG API key connected through OOMOL, and RAWG queries and results pass through the OOMOL connector service. <br>
Mitigation: Use it only with an approved OOMOL-connected RAWG account and avoid exposing raw credentials to the agent. <br>
Risk: First-time use may require installing and signing in to the oo CLI. <br>
Mitigation: Follow OOMOL setup documentation and run authentication or connection steps only after an auth or connection error. <br>


## Reference(s): <br>
- [ClawHub RAWG skill page](https://clawhub.ai/oomol/oo-rawg) <br>
- [RAWG homepage](https://rawg.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration instructions, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [RAWG results are returned through the OOMOL connector with execution metadata when commands are run with --json.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence release version and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
