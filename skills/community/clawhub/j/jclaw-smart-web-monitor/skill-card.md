## Description: <br>
Smart Web Monitor watches web pages for keyword, regex, CSS, JSONPath, or agent-judged natural-language matches and helps report or pause monitors after a match. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skywalker-lili](https://clawhub.ai/user/skywalker-lili) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to create scheduled web monitors that fetch public pages, evaluate configured matching rules, and surface relevant changes or extracted page text for agent review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: LLM-mode monitors can place extracted page text into the agent's reasoning context and local reports or logs. <br>
Mitigation: Use LLM mode only for public or low-sensitivity pages, and avoid private dashboards, authenticated pages, secrets, personal data, or proprietary content. <br>
Risk: Cron jobs can repeatedly fetch monitored pages and trigger agent review without direct user interaction. <br>
Mitigation: Review each cron job before enabling it and confirm the monitored URLs and notification behavior are intended. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/skywalker-lili/jclaw-smart-web-monitor) <br>
- [Hacker News example monitor](https://news.ycombinator.com/) <br>
- [HKMA vacancies example monitor](https://www.hkma.gov.hk/chi/about-us/join-us/current-vacancies/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON monitor configuration, JSON fetch output, and Markdown reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetch output caps extracted page text at about 20000 characters per URL before agent review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
