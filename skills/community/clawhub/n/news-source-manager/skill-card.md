## Description: <br>
Manages user's news category preferences and information sources, stores them in news-sources.json, and supports add, remove, list, and export operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kedoupi](https://clawhub.ai/user/kedoupi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Professionals, investors, founders, research teams, and other OpenClaw users use this skill to configure news categories and preferred sources for personalized briefings and related news workflows such as insight-radar. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A user may remove categories or change preferred source lists in a way that makes later news briefings less relevant. <br>
Mitigation: Review proposed before-and-after changes before confirming removals or source updates. <br>
Risk: Configured sources can affect the balance and quality of downstream news results. <br>
Mitigation: Prefer clearly named, trusted sources and periodically review active categories and source priorities. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kedoupi/news-source-manager) <br>
- [keyword-templates.json](references/keyword-templates.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, JSON] <br>
**Output Format:** [Markdown guidance and JSON configuration data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and reads local news preference configuration in news-sources.json after user confirmation.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
