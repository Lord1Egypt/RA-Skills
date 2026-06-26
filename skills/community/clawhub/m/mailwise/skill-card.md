## Description: <br>
Search and analyze email issue threads from a local knowledge base to find past bugs, incidents, root causes, and similar resolutions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[petrguan](https://clawhub.ai/user/petrguan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and support engineers use MailWise to search indexed local EML archives for similar past bugs, incidents, and expert debugging threads, then optionally request Claude-generated analysis over selected excerpts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MailWise operates on private local email archives, which may include sensitive business or personal information. <br>
Mitigation: Install and use it only when you are allowed to index the selected email archives, and apply your organization's data handling policy before searching or showing messages. <br>
Risk: The analyze command sends relevant email excerpts to Anthropic through Claude for external analysis. <br>
Mitigation: Use analyze only when external processing is permitted; review or redact sensitive content first, and prefer local search/show commands when external analysis is not allowed. <br>


## Reference(s): <br>
- [MailWise ClawHub listing](https://clawhub.ai/petrguan/mailwise) <br>
- [MailWise homepage](https://github.com/PetrGuan/MailWise) <br>
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and terminal text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local search, show, stats, and expert-management commands operate on indexed email archives; analyze requires Claude Code authentication or ANTHROPIC_API_KEY.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
