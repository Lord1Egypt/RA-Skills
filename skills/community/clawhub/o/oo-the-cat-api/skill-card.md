## Description: <br>
The Cat API skill helps agents search and read cat breed and image data through the OOMOL `oo` CLI and `the_cat_api` connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill when they need an agent to look up The Cat API breeds and images through an OOMOL-connected account instead of calling the API directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an installed and authenticated OOMOL oo CLI connection to The Cat API. <br>
Mitigation: Run installer, login, or connection steps only when a command fails for that specific setup reason. <br>
Risk: Future connector actions may add write or destructive behavior. <br>
Mitigation: Inspect the live action schema and obtain explicit user approval before running any action that writes, deletes, or overwrites data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-the-cat-api) <br>
- [The Cat API homepage](https://thecatapi.com/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only connector actions for breed and image lookup; requires an installed and authenticated OOMOL oo CLI connection.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
