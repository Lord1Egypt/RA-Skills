## Description: <br>
快导(KD) helps agents generate, validate, and manage batches of short-video scripts and copy-library entries across platforms such as Xiaohongshu, Douyin, and WeChat Channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gitgily](https://clawhub.ai/user/gitgily) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators, creators, and agents use this skill to run a 10-step workflow that researches short-video trends, reads platform rules, generates differentiated scripts, validates the outputs, writes them to an Excel copy library, and produces a Markdown report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Feishu integration requests broad workspace permissions, including tenant-wide messaging, app management, chat, file, document, wiki, and spreadsheet scopes. <br>
Mitigation: Review and reduce Feishu scopes before use, provide LARK_CLI_TOKEN only when upload features are required, and keep reporting local when wiki publishing is unnecessary. <br>
Risk: Generated reports may include internal paths, configuration details, or generated content before optional publishing. <br>
Mitigation: Inspect reports before publishing to Feishu and redact internal paths, configuration values, and sensitive generated content. <br>
Risk: User-configured Excel copy-library and platform-rules paths could target unintended files or directories. <br>
Mitigation: Configure copy_library_path and rules_path only to files and directories the user controls, and avoid system or shared directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gitgily/kuaidao) <br>
- [Skill README](artifact/README.md) <br>
- [Runtime references guide](artifact/references/README.md) <br>
- [Platform rules guide](artifact/references/platform_rules/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; executed workflows may update Excel workbooks and produce Markdown reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local configuration for platform keywords, copy-library paths, and optional Feishu reporting.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
