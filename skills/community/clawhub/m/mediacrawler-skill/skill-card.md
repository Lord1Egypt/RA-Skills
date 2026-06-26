## Description: <br>
基于 MediaCrawler 的多平台公开信息采集工具，支持安装、命令行运行、WebUI、结果定位与常用任务模板。 <br>

This skill is for research and development only. <br>

## Publisher: <br>
[Excalibur9527](https://clawhub.ai/user/Excalibur9527) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install and run MediaCrawler-based collection workflows for public social platform content, including keyword search, detail collection, creator collection, WebUI operation, and result discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation downloads and executes external setup code, installs dependencies and a browser, and modifies $HOME/MediaCrawler. <br>
Mitigation: Review the setup script and upstream repository before installation, and run setup in a container or isolated user account when possible. <br>
Risk: Crawler runs can retain collected data and possibly login or session state on disk. <br>
Mitigation: Use a dedicated workspace, inspect configured output paths, and manually remove result files and cached session data after use. <br>
Risk: Collection workflows may interact with third-party social platforms and can create legal, policy, or privacy risk if misused. <br>
Mitigation: Confirm each planned collection task is lawful, authorized, and compliant with applicable platform terms before execution. <br>


## Reference(s): <br>
- [Media Crawler ClawHub listing](https://clawhub.ai/Excalibur9527/mediacrawler-skill) <br>
- [MediaCrawler upstream repository](https://github.com/NanmiCoder/MediaCrawler.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides setup, crawler execution, WebUI launch, and result file lookup; crawler data is written by the installed MediaCrawler project.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release evidence and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
