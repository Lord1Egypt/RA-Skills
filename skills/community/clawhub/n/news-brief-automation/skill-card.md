## Description: <br>
Build, refine, or maintain recurring news-digest workflows that periodically collect items from sources such as Hacker News, GitHub Trending, Hugging Face, RSS feeds, blogs, and specific news sites; deduplicate against the newest prior report; save a Markdown brief in the workspace; and send the same summary to the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[louishwh](https://clawhub.ai/user/louishwh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and knowledge workers use this skill to create reusable scheduled prompts for daily or intraday news briefs. It helps agents gather configured sources, deduplicate against prior saved reports, save Markdown output in the workspace, and send the same summary to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated automations may include unsuitable sources, cadence, save paths, or delivery targets. <br>
Mitigation: Confirm the source list, schedule, report path, and delivery target before enabling recurring use. <br>
Risk: Generated prompts or reports may expose sensitive links or credentials if those are included in automation inputs. <br>
Mitigation: Avoid placing private credentials or sensitive URLs in generated news-brief prompts or reports. <br>


## Reference(s): <br>
- [Examples](references/examples.md) <br>
- [Templates](references/templates.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/louishwh/news-brief-automation) <br>
- [Hacker News](https://news.ycombinator.com/) <br>
- [Hacker News Newest](https://news.ycombinator.com/newest) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown prompt templates and Markdown news brief reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs commonly include cron prompt files under automation/cron/ and dated reports under reports/.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
