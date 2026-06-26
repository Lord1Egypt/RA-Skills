## Description: <br>
TinyURL (tinyurl.com). Use this skill for ANY TinyURL request — reading, creating, and updating data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to operate TinyURL through an OOMOL-connected account, including creating short links and listing account URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create TinyURL links through the user's connected account. <br>
Mitigation: Confirm the destination URL and intended effect with the user before running `create_short_url`. <br>
Risk: The skill depends on an OOMOL account connection and may require trusted setup steps. <br>
Mitigation: Run CLI installation, login, or TinyURL connection setup only when needed and only through the documented OOMOL setup paths. <br>
Risk: TinyURL actions may require sensitive credentials managed outside the agent. <br>
Mitigation: Use the OOMOL connector flow so credentials remain server-side and are not handled directly in prompts or shell payloads. <br>


## Reference(s): <br>
- [TinyURL homepage](https://tinyurl.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL TinyURL connection setup](https://console.oomol.com/app-connections?provider=tinyurl) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas and returns connector responses as JSON when actions run.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
