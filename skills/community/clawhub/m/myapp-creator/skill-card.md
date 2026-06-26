## Description: <br>
Create or update standalone single-file HTML apps and documents from user requests, then save them to fe-service without invoking an LLM directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhang6714268](https://clawhub.ai/user/zhang6714268) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn a user's app or document request into self-contained HTML, then register or update that generated content through the publisher service. It is intended for ClawHub/OpenClaw app-creation flows that need installation checks, creation, update, and lookup tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated apps, documents, and device or user identifiers are sent to the publisher service. <br>
Mitigation: Install and use this skill only when that transfer is expected, and avoid sensitive personal or business content unless the publisher service's retention and access controls are trusted. <br>
Risk: The local MYAPP_API_TOKEN is a long-lived credential stored in user configuration. <br>
Mitigation: Protect local configuration files and rotate the token if the machine or configuration may have been shared. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhang6714268/myapp-creator) <br>
- [README](artifact/README.md) <br>
- [Tool Schema](artifact/openai.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance, shell commands, JSON tool arguments, and single-file HTML content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated HTML is expected to be self-contained, no larger than 60KB, compatible with Android 8.1 WebView, and submitted through the skill tools.] <br>

## Skill Version(s): <br>
1.0.31 (source: server release metadata, clawhub.yaml, metadata.json, version.txt) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
