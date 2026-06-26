## Description: <br>
Deploys an automated three-agent translation pipeline for extracting source content, translating it between languages, and reviewing translations before publication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and localization operators use this skill to configure three coordinated agents that extract source material, translate it, and route approved translations to downstream systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup depends on local pilotctl and clawhub binaries and installs additional pilot skills. <br>
Mitigation: Confirm the binaries and each pilot skill are trusted before installation or execution. <br>
Risk: Incorrect or untrusted handshakes could route translation content to unintended peers. <br>
Mitigation: Use trusted handshakes only and verify peer hostnames before subscribing or publishing. <br>
Risk: External webhook publication can expose confidential or regulated translation content. <br>
Mitigation: Configure webhook destinations carefully and use privacy, redaction, and audit controls before processing sensitive content. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-translation-pipeline-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON manifest examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces role-specific setup instructions for extractor, translator, and reviewer agents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
