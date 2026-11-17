## Description:

IndustryInformation queries FEEDAX industry news and public-opinion data by keyword, industry classification, sentiment, and popularity to help agents summarize industry trends and risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longgggggg](https://clawhub.ai/user/longgggggg)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to monitor industry news, compare sector sentiment, assess emerging risks, and export query results for further review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials may be exposed through unsafe key handling.

Mitigation: Use a secure environment variable or secret store, do not paste keys into chat, do not print `.env`, and rotate any FEEDAX key already used with this version.

Risk: The server security summary reports plaintext HTTP transmission for API requests.

Mitigation: Use this skill only after the endpoint is changed to HTTPS or the request path is otherwise protected for the deployment environment.

Risk: Industry news and sentiment outputs can be incomplete, stale, or unsuitable as sole support for investment or risk decisions.

Mitigation: Treat results as monitoring inputs and verify important claims against authoritative sources before acting on them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/longgggggg/skills/industry-information)
- [FEEDAX](https://www.feedax.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration guidance]

**Output Format:** [Conversation summaries plus generated CSV and Markdown result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a FEEDAX API key and returns time-bounded industry news, sentiment, classification, importance, and popularity fields.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
