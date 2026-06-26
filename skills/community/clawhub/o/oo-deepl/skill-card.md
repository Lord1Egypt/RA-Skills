## Description: <br>
Use DeepL through an OOMOL-connected account to translate text, list supported languages, and fetch API usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to operate DeepL through the OOMOL oo CLI for translation, supported-language lookup, and API usage checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Translation text and usage requests are sent through the connected DeepL/OOMOL integration. <br>
Mitigation: Confirm the user is comfortable using the OOMOL oo CLI and DeepL connector before installation or first use. <br>
Risk: First-time setup may install the oo CLI and create a persistent login session. <br>
Mitigation: Run setup steps only after an auth, connection, or missing-command failure and follow the artifact's setup guidance. <br>


## Reference(s): <br>
- [DeepL homepage](https://www.deepl.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub DeepL skill page](https://clawhub.ai/oomol/oo-deepl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return normalized DeepL connector JSON containing action data and an execution id.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
