## Description: <br>
Guides users through OpenClaw Diary initialization, including personality selection, optional identity setup, storage configuration, authorization collection, and configuration-file creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smorzandos](https://clawhub.ai/user/smorzandos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to initialize a diary workspace, choose a diary assistant style, configure local or cloud-backed storage, and optionally create a user identity profile from chat or imported documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow can install tools and dependent skills and create local files. <br>
Mitigation: Review proposed shell commands and generated paths before execution, and prefer the local-only setup path when cloud sync is not required. <br>
Risk: The skill may request service credentials such as Feishu app secrets, Notion tokens, and Flomo API tokens. <br>
Mitigation: Use narrowly scoped tokens, avoid pasting long-lived secrets into chat, and store credentials in a dedicated secret manager or reviewed environment configuration. <br>
Risk: Optional imports can bring personal or workspace data into the diary memory area. <br>
Mitigation: Import only the sources needed for the diary setup, avoid all-source imports, and inspect generated identity and memory files before relying on them. <br>
Risk: Generated configuration and shell-profile changes can affect later diary behavior or sync destinations. <br>
Mitigation: Inspect the generated configuration file and any suggested shell-profile edits before reloading the shell or enabling cloud synchronization. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smorzandos/openclaw-diary-setup) <br>
- [OpenClaw Diary homepage](https://github.com/openclaw-community/diary-system) <br>
- [Digital Life Import guide](importers/digital_life_import.md) <br>
- [Feishu user profile importer guide](importers/feishu_importer.md) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>
- [Notion Integrations](https://www.notion.so/my-integrations) <br>
- [Flomo](https://flomoapp.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local diary directories, configuration JSON, identity Markdown, and shell environment-variable snippets.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
