## Description: <br>
AiVOOV helps agents use an OOMOL-connected AiVOOV account to list voices and generate audio through the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when an agent needs to work with AiVOOV via an OOMOL-connected account, including browsing available voices and generating audio from voice/text segments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected AiVOOV account and uses account credentials through the OOMOL connection flow. <br>
Mitigation: Install it only when the user intends to use AiVOOV through OOMOL, and rely on the OOMOL account connection flow rather than exposing raw tokens. <br>
Risk: The create_audio action is a write action and may consume account credits. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running create_audio, and stop on billing or insufficient-credit errors. <br>
Risk: First-time setup may require installing or authenticating the oo CLI. <br>
Mitigation: Review the oo CLI installer and run setup only when commands fail with a matching install, authentication, or connection error. <br>


## Reference(s): <br>
- [ClawHub AiVOOV release](https://clawhub.ai/oomol/oo-aivoov) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [AiVOOV homepage](https://aivoov.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Action responses are JSON from the oo CLI and may include generated audio data plus execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
