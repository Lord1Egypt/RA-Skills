## Description: <br>
MailMe X News fetches X/Twitter posts, translates them into Chinese with AI, generates a digest, and sends the result by email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyingtimes](https://clawhub.ai/user/flyingtimes) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Operators or developers use this skill to automate an X/Twitter news digest workflow: collect posts, translate and summarize them in Chinese, combine the results, and email the completed Markdown digest. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can automatically send scraped and summarized content to preset real email recipients without a clear per-run confirmation step. <br>
Mitigation: Replace preset recipients, verify the dependent crawl and email skills, and require a manual preview or explicit confirmation before any run sends email, especially before enabling the daily cron task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flyingtimes/mailme-x-news) <br>
- [Publisher profile](https://clawhub.ai/user/flyingtimes) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with configuration snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces timestamped Markdown post captures, Chinese translations, summary files, combined digest files, and email-send guidance.] <br>

## Skill Version(s): <br>
1.6.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
