## Description: <br>
Provides latest news summaries with titles, sources, and brief overviews for user-supplied topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loverun321](https://clawhub.ai/user/loverun321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to request recent news summaries for a topic and receive a small set of summarized results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports a live-looking payment key and possible paid billing without clear per-call user control. <br>
Mitigation: Rotate and remove the exposed payment key, store credentials outside the skill artifact, and require explicit user consent and spending controls before each paid call. <br>
Risk: The release evidence advises correcting the news-provider disclosure before users rely on the skill. <br>
Mitigation: Update the public description and artifact behavior so the disclosed news source matches the actual provider used for retrieval. <br>
Risk: The security verdict is suspicious despite ordinary news functionality. <br>
Mitigation: Review the skill before installation and publish clear billing, data-sharing, and provider disclosures for users. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/loverun321/news-skill) <br>
- [Publisher profile](https://clawhub.ai/user/loverun321) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [JSON-like response containing topic, news items, item count, and payment status or error fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [News results are limited to a small list of items with truncated titles and summaries.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
