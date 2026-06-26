## Description: <br>
Aggregates recent China and Guangdong computing power and AI policy updates, including large models, intelligent computing centers, data centers, and public bond support, into briefing-style summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwrry](https://clawhub.ai/user/wwrry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Policy researchers, business teams, and public-sector analysts use this skill to find and summarize recent Guangdong, Guangzhou, Shenzhen, and China national policy updates related to computing infrastructure, AI models, intelligent computing centers, data centers, and government bond support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill searches and fetches public government or media pages, which may expose outbound queries to configured search providers. <br>
Mitigation: Review the agent environment's search and fetch providers before deployment when query logging, network routing, or compliance requirements matter. <br>
Risk: Policy briefings may omit recent items if search providers fail or if public sources are delayed. <br>
Mitigation: Prefer official government source links in the generated briefing and manually confirm critical policy decisions against the cited source pages. <br>


## Reference(s): <br>
- [Guangdong computing policy source list](references/policy_sources.md) <br>
- [ClawHub skill page](https://clawhub.ai/wwrry/guangdong-computing-policy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown briefing with source links, publication dates, and grouped policy summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Searches recent public government and authoritative media sources and reports when no matching recent policy is found.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
