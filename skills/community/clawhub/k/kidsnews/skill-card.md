## Description: <br>
Generates a daily 09:00 Simplified Chinese KidsNews brief with child-friendly summaries, thinking questions, debate prompts, and links to full articles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shujip](https://clawhub.ai/user/shujip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Families and parents use this skill to receive a concise daily Chinese news brief suitable for children. The brief helps start guided conversations with summaries, reflection questions, debate topics, and links for deeper reading or listening. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The brief depends on kidsnews.app as the source of news content. <br>
Mitigation: Install only if the user trusts kidsnews.app as a source and keep links visible for review. <br>
Risk: Linked news content may not always match every child's age or family context. <br>
Mitigation: Parents should review linked content for age suitability before relying on it with children. <br>
Risk: A daily 09:00 delivery workflow can reach users through an inappropriate or poorly timed channel. <br>
Mitigation: Choose a delivery channel and timezone that are appropriate for the receiving family. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shujip/kidsnews) <br>
- [KidsNews daily report API](https://www.kidsnews.app/api/kidsnews/daily-report) <br>
- [KidsNews site](https://www.kidsnews.app) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance, Configuration] <br>
**Output Format:** [Simplified Chinese Markdown-style daily brief with article links, questions, and a debate topic] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches a public KidsNews feed, selects up to three eligible items, and avoids adding unsupported facts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
