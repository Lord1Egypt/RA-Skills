## Description: <br>
ElevenReader lets agents use an OOMOL-connected ElevenReader account to search voices, retrieve speech models and account information, and convert text to speech. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to operate ElevenReader through OOMOL from an agent, including voice search, model lookup, profile and subscription checks, and text-to-speech generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected OOMOL account and may rely on ElevenReader credentials for connector actions. <br>
Mitigation: Only approve setup or connection steps when the user is comfortable linking ElevenReader credentials to OOMOL, and do not repeat authentication setup unless a command fails for that reason. <br>
Risk: Text submitted for speech generation may be sent to the connector service and converted audio is uploaded to connector transit storage. <br>
Mitigation: Send only text that is appropriate for the connected service and review the payload before running text-to-speech actions. <br>


## Reference(s): <br>
- [ClawHub ElevenReader skill page](https://clawhub.ai/oomol/oo-elevenreader) <br>
- [ElevenReader homepage](https://elevenlabs.io/text-reader) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON payloads; connector responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads; read_text returns generated audio through connector transit storage.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
