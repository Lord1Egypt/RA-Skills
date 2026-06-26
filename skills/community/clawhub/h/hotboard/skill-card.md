## Description: <br>
OpenClaw skill for fetching hot trending data from multiple platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[llnancy](https://clawhub.ai/user/llnancy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Hotboard to choose relevant trend platforms and fetch hot topics from news, technology, developer, entertainment, gaming, sports, reading, international, and utility sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs an external Hotboard PyPI CLI whose full package source is not included in the submitted skill text. <br>
Mitigation: Review the package and installation path before deployment, and only install it in environments where the publisher and package source are trusted. <br>
Risk: Trend results from third-party platforms may be incomplete, stale, biased, or otherwise not verified facts. <br>
Mitigation: Treat fetched trend data as signals for exploration and verify important claims against authoritative sources before acting on them. <br>


## Reference(s): <br>
- [Hotboard Skill on ClawHub](https://clawhub.ai/llnancy/hotboard) <br>
- [llnancy Publisher Profile](https://clawhub.ai/user/llnancy) <br>
- [hotboard PyPI package](https://pypi.org/project/hotboard/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with inline hotboard commands and optional markdown or JSON trend data from the CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on the external hotboard CLI and third-party platform availability.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
