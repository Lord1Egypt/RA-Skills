## Description: <br>
Run Promarkia AI squads via the Promarkia API for social media posts, copywriting, SEO, ads, lead generation, image and video creation, campaign planning, and related marketing automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dominiclachance](https://clawhub.ai/user/dominiclachance) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run Promarkia squads from an agent or command line, including one-off marketing jobs and scheduled recurring automations. It requires a Promarkia API key and may operate connected publishing, analytics, lead generation, or content accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run paid Promarkia automations and deduct credits from the user's account. <br>
Mitigation: Use a dedicated API key, monitor credit usage, and review task prompts before submitting long-running or recurring work. <br>
Risk: Publishing-capable squads can post through connected social, document, lead generation, or video accounts. <br>
Mitigation: Connect only the accounts needed for the intended workflow, keep permissions least-privileged, and review outputs before enabling publish-capable tasks. <br>
Risk: Recurring cron tasks can continue operating without ongoing manual review. <br>
Mitigation: Regularly list and remove unneeded cron jobs, and require periodic review for any recurring automation. <br>


## Reference(s): <br>
- [ClawHub Promarkia Skill Page](https://clawhub.ai/dominiclachance/promarkia) <br>
- [Promarkia Website](https://www.promarkia.com) <br>
- [Promarkia Blog and Documentation](https://blog.promarkia.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown and terminal output from Promarkia API requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return squad results, run IDs, credit and token usage, errors, or status messages for long-running tasks.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
