## Description: <br>
Gamma (gamma.app). Use this skill for ANY Gamma request: reading, creating, and updating data through the OOMOL Gamma connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate Gamma through an OOMOL-connected account, including creating generations, checking generation status, and listing available folders or themes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected Gamma account and may use sensitive account credentials handled through the OOMOL flow. <br>
Mitigation: Install and use it only if you trust the OOMOL oo CLI and connect Gamma through the expected OOMOL connection page. <br>
Risk: Generation actions can create or update Gamma state based on user-provided payloads. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running any write action. <br>
Risk: Setup commands include remote installer URLs for the oo CLI. <br>
Mitigation: Review the installer before execution and prefer the documented platform-specific install path. <br>


## Reference(s): <br>
- [ClawHub Gamma Skill](https://clawhub.ai/oomol/oo-gamma) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Gamma](https://gamma.app) <br>
- [Gamma Connector Setup](https://console.oomol.com/app-connections?provider=gamma) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON payloads and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return Gamma generation status, result URLs, folder lists, theme lists, or setup guidance depending on the selected connector action.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
