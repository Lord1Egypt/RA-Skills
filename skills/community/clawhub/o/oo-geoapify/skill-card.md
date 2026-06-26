## Description: <br>
Geoapify helps agents use Geoapify through the OOMOL oo CLI for address autocomplete, geocoding, routing, and travel matrix workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to operate Geoapify through an OOMOL-connected account for place lookup, forward and reverse geocoding, route calculation, and travel matrix generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive credentials through an OOMOL-connected Geoapify account. <br>
Mitigation: Install and use it only when you intend to operate Geoapify through OOMOL, and run account connection steps only when an auth or connection error requires setup. <br>
Risk: Connector actions can run with user-provided JSON payloads, and actions tagged as write may change Geoapify state. <br>
Mitigation: Inspect the live action schema before constructing payloads, review payloads before execution, and confirm the exact effect with the user before write or destructive actions. <br>


## Reference(s): <br>
- [Geoapify homepage](https://www.geoapify.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-geoapify) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live action schema inspection before running Geoapify connector actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
