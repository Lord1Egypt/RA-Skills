## Description:

Liurun Fetcher helps an agent fetch recent Liu Run WeChat public-account articles through Sogou/WeChat access paths and produce structured daily business summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolfzb](https://clawhub.ai/user/coolfzb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to monitor Liu Run's public WeChat content and receive concise summaries, key insights, personalized business implications, and trend judgments. It is suited to recurring business-news briefings where the user explicitly wants WeChat/Sogou retrieval and local summary archives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports unsafe network-fetching code.

Mitigation: Review the fetch helpers before use, require HTTPS, restrict allowed hosts to intended WeChat and Sogou endpoints, and limit redirects.

Risk: The security guidance warns against granting portfolio access or enabling scheduled runs without explicit intent.

Mitigation: Run the skill only with the minimum data access needed, keep financial or portfolio data out of routine summaries unless deliberately supplied, and approve any scheduled execution separately.

Risk: The security verdict is suspicious because the skill combines WeChat article summarization with requests to use and persist investment holdings.

Mitigation: Treat personalized financial implications as user-provided context, review generated summaries before relying on them, and avoid storing sensitive holdings unless retention is required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/coolfzb/skills/liurun-fetcher)
- [Publisher Profile](https://clawhub.ai/user/coolfzb)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summaries with optional saved text or HTML files from fetch helpers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries usually include a one-sentence summary, five key insights, personalized implications, and trend judgments.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
