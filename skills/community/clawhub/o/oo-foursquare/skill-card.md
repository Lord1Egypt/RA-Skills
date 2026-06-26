## Description: <br>
Foursquare helps agents search and read Foursquare place data through the OOMOL connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search Foursquare places, retrieve nearby venues, and read place details, photos, and tips through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected Foursquare account and may prompt setup or login steps if authentication fails. <br>
Mitigation: Install only if OOMOL is an acceptable connector layer, avoid repeating one-time login or install steps unless commands fail, and follow the security guidance for authentication and connection errors. <br>
Risk: Future connector actions could be marked write or destructive even though the current listed Foursquare actions are read operations. <br>
Mitigation: Inspect the live connector schema before running actions and confirm any write or destructive action, target, and payload with the user before execution. <br>


## Reference(s): <br>
- [Foursquare homepage](https://foursquare.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-foursquare) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before action execution; connector responses are JSON when run with --json.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
