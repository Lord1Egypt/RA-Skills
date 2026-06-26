## Description: <br>
Generate images via Krea.ai API (Flux, Imagen, Ideogram, Seedream, etc.). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FossilizedCarlos](https://clawhub.ai/user/FossilizedCarlos) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to generate images through Krea.ai models, inspect recent jobs, and open account usage information while using a local credential file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Krea API credentials can be exposed if secrets are passed on the command line or printed from the credential file. <br>
Mitigation: Use the documented credential file at ~/.openclaw/credentials/krea.json with chmod 600, prefer a dedicated or revocable Krea API key, and avoid displaying the file contents. <br>
Risk: Image generation requests may consume Krea account credits. <br>
Mitigation: Monitor Krea usage through the account dashboard and review prompts and generation parameters before running jobs. <br>


## Reference(s): <br>
- [Krea API Keys and Billing](https://docs.krea.ai/developers/api-keys-and-billing) <br>
- [Krea Usage Statistics](https://www.krea.ai/settings/usage-statistics) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return image URLs, job status summaries, model lists, and credential setup instructions.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
