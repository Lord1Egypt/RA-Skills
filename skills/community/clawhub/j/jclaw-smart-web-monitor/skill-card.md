## Description:

Smart Web Monitor lets an agent monitor web pages using keyword, regex, CSS, JSONPath, or LLM-based natural-language matching, with commands to create, run, fetch, pause, resume, enable, disable, and delete monitors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skywalker-lili](https://clawhub.ai/user/skywalker-lili)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to watch public web pages for matching content, summarize matches, and manage monitor state through local configuration and OpenClaw cron jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary user-configured URLs and process untrusted page text.

Mitigation: Use monitors only with trusted public URLs and avoid authenticated, private, or internal dashboards.

Risk: LLM-based monitors feed web page content to a command-capable cron agent.

Mitigation: Add strong confirmation and prompt-injection safeguards before scheduling LLM-based monitors.

Risk: Scheduled monitors can create recurring tasks, local files, and outbound summaries.

Mitigation: Review cron messages, destination channels, and generated monitor configuration before enabling recurring execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skywalker-lili/skills/jclaw-smart-web-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, JSON monitor data, and Markdown alert reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetch output caps extracted page text at about 20000 characters per URL for LLM review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
