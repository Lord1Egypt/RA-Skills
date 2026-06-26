## Description: <br>
Tracks Toutiao hot-news rankings and searches Toutiao news by keyword for current topics and related articles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huyi9531](https://clawhub.ai/user/huyi9531) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People using an agent to monitor current Chinese news trends can ask for Toutiao hot lists or keyword-based news results with summaries, media sources, timestamps, and links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on an external gnomic CLI package and sends news search terms to that service. <br>
Mitigation: Install the CLI only after trusting the package, and avoid using the skill for sensitive private topics. <br>
Risk: Live news rankings and search results can change quickly and may be incomplete or source-dependent. <br>
Mitigation: Check timestamps and source links before relying on results for decisions or redistribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huyi9531/hot-news-tracker) <br>
- [gnomic-cli repository](https://github.com/huyi9531/gnomic_cli) <br>
- [Toutiao](https://www.toutiao.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with links and optional shell commands; the source CLI can return JSON or text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Freshness and result coverage depend on Toutiao data and the external gnomic CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
