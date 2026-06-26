## Description: <br>
Hita-Mind & Knowledge helps AI agents store and retrieve long-term memories and knowledge through a local Mind Module and Knowledge Manager. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hita126](https://clawhub.ai/user/hita126) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to maintain local long-term agent memory, retrieve past preferences and decisions, and build knowledge context from stored tips, methods, rules, and project experience. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages local long-term storage of user preferences, contacts, project details, and daily notes without clear consent or retention controls. <br>
Mitigation: Review where the JSON stores are kept, define consent and retention expectations before use, and inspect or delete entries regularly. <br>
Risk: Sensitive information could be captured in local memory or knowledge entries. <br>
Mitigation: Do not store secrets, credentials, regulated personal data, customer data, or confidential project details unless the storage and deletion process has been reviewed. <br>


## Reference(s): <br>
- [Hita-Mind & Knowledge on ClawHub](https://clawhub.ai/hita126/hita-mind-knowledge) <br>
- [Root README](README.md) <br>
- [Mind Module README](hita-mind-module/README.md) <br>
- [Knowledge Manager README](hita-knowledge-manager/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [CLI text and Markdown-like context blocks backed by local JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists memory and knowledge entries to local JSON stores.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
