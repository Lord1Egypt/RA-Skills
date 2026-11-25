## Description:

Uses public Douyin data to search videos, creators, posts, comments, and trends, then returns structured JSON for content research and lead analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, content, and growth teams can use this skill to research public Douyin videos, creators, comments, and trends. It returns structured data that supports topic selection, competitor research, sentiment and demand analysis, and public lead qualification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and supplied Douyin URLs or IDs are sent to the GuaiKei third-party API; its guidance also notes additional account and trend search features.

Mitigation: Before querying, confirm the user is comfortable sharing those inputs with the service and keep searches within the requested public-data scope.

Risk: The security assessment reports medium confidence and partial component analysis.

Mitigation: Review the skill and its account and trend search features before installation or use.

## Reference(s):

- [GuaiKei API and support](https://www.guaikei.com)
- [Public lead research workflow](artifact/references/customer-acquisition.md)
- [Output contract](artifact/references/contract.md)
- [ClawHub skill release](https://clawhub.ai/engheng-art/skills/huo-ke)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON result envelopes with concise text analysis or lead summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results may be saved as JSON under the skill directory; the agent should summarize relevant fields rather than reproduce entire result sets.]

## Skill Version(s):

1.4.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
