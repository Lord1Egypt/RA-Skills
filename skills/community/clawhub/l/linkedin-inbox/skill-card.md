## Description: <br>
Manages LinkedIn inbox monitoring, message classification, user-style draft replies, approval workflows, and scheduled summaries through browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dylanbaker24](https://clawhub.ai/user/dylanbaker24) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and business operators use this skill to monitor LinkedIn messages, prepare replies that match their communication style, and send only approved responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can monitor private LinkedIn messages and expose message details through screenshots, logs, or notification channels. <br>
Mitigation: Use a dedicated browser profile, close unrelated sensitive tabs, keep notification channels private, and review captured content handling. <br>
Risk: Browser-control automation can send messages from a logged-in LinkedIn account. <br>
Mitigation: Require explicit approval for each recipient and draft, avoid broad commands such as send all, and keep action limits enabled. <br>
Risk: Scheduled monitoring may continue after it is no longer needed. <br>
Mitigation: Remove heartbeat or cron entries when monitoring ends and keep scans within configured active hours. <br>


## Reference(s): <br>
- [Communication Style Extraction Guide](references/style-extraction.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/dylanbaker24/linkedin-inbox) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples, shell command snippets, notification summaries, and draft reply text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Human approval is required before sending messages; screenshots, logs, and notification summaries may contain private LinkedIn message content.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
